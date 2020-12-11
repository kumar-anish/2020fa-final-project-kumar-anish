import os
import pandas as pd
from csci_utils.io.io import atomic_write


def excel_2_parquet(data):
    pd_df = pd.read_excel(data)
    df_name, df_ext = os.path.splitext(data)
    parquet_path = df_name + ".parquet"

    with atomic_write(parquet_path, mode="w", as_file=False) as f:
        pd_df.to_parquet(f)

    return parquet_path


if __name__ == "__main__":
    data_source = "/Users/ka/2020fa-final-project-kumar-anish/data/query_logs.xlsx"
    parquet_file = excel_2_parquet(data_source)
    query_id = pd.read_parquet(parquet_file, columns=["QueryID"])
    print(query_id)
