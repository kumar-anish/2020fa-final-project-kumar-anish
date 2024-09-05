import numpy as np
import pandas as pd

##add some comments
def load_words(filename):
    """Load a file containing a list of words as a python list

    use case: data/words.txt

    :param str filename: path/name to file to load
    :rtype: list
    """
    with open(filename, 'r') as f:
        words = f.read().split()

    return words


def load_vectors(filename):
    """Loads a file containing word vectors to a python numpy array

    use case: `data/vectors.npy.gz`
    :param str filename:

    :returns: 2D matrix with shape (m, n) where m is number of words in vocab
        and n is the dimension of the embedding

    :rtype: ndarray
    """
    return np.load(filename)


def load_data(filename):
    """Load student response data in parquet format

    use case: data/project.parquet
    :param str filename:

    :returns: dataframe indexed on a hashed github id
    :rtype: DataFrame
    """
    # You will probably need to fill a few NA's and set/sort the index via
    # pandas
    df = pd.read_parquet(filename, engine='pyarrow')
    fillna_df = df.fillna(0, axis=0)
    return fillna_df
#
