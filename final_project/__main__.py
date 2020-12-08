import os
import pandas as pd

from .hash_str import hash_str, get_csci_salt, get_user_id
from .io import atomic_write


def get_user_hash(username, salt=None):
    salt = salt or get_csci_salt()
    return hash_str(username, salt=salt)


def excel_2_parquet(data):
    pd_df = pd.read_excel(data)
    df_name, df_ext = os.path.splitext(data)
    parquet_path = df_name + ".parquet"

    with atomic_write(parquet_path, mode="w", as_file=False) as f:
        pd_df.to_parquet(f)

    return parquet_path


if __name__ == "__main__":

    for user in ["gorlins", "kumar-anish"]:
        print("Id for {}: {}".format(user, get_user_id(user)))

    data_source = "data/hashed.xlsx"
    parquet_file = excel_2_parquet(data_source)
    hashed_id = pd.read_parquet(parquet_file, columns=["hashed_id"])
    print(hashed_id)
