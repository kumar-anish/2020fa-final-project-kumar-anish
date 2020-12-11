import os
import pandas as pd

from dotenv import load_dotenv

from final_project.data import load_data
from final_project.embedding import WordEmbedding, cosine_distance, delete_files, cosine_similarity
from .io import atomic_write

load_dotenv()


def main(args=None):

    # read in the hashed student data
    data = load_data("data/query_logs.parquet")

    def my_distance(vec):
        return 1 - cosine_similarity(vec, my_embed_vec)

    # read my sql keywords text from ENV variable "MY_SQL_QUERY_MATCH_TEXT" , since its not available in project.parquet
    my_sql_match_text = os.environ.get('MY_SQL_QUERY_MATCH_TEXT')

    # utilize atomic_write to export results to data
    filename = "data/QueryMatchResults.parquet"
    if os.path.exists(filename):
        df_dist_to_peers = load_data(filename)
        distances = pd.Series(df_dist_to_peers['QueryText'])
    else:
        embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')
        vectors = data['QueryText'].apply(embedding.embed_document)
        # Calculate the distance
        my_embed_vec = WordEmbedding.embed_document(embedding, my_sql_match_text)
        distances = vectors.apply(my_distance)
        distances = distances[pd.notnull(distances)]
        distances = distances[abs(distances) > 1e-10]
        with atomic_write(filename, mode="w", as_file=False) as f:
            (pd.DataFrame(distances)).to_parquet(f)


    # find matching sqls with those keywords
    # print a summary of yourself and the top 4 most similar query using these keywords
    print('my_matched_sql_keywords_text:')
    print(my_sql_match_text)
    print('\n')

    print('top 4 similar sql texts: \n')
    distances = distances.sort_values()
    count = 0
    for i in distances.index:
        print('id          : {}'.format(i))
        print('distance    : {}'.format(distances.loc[i]))
        print('QueryText text:')
        print(data.loc[i]['QueryText'])
        print('\n')
        count = count + 1
        if count == 4:
            break


if __name__ == "__main__":
    main()
