#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `final_project` package."""

import os
import io
from tempfile import TemporaryDirectory
from unittest import TestCase, mock
import pandas as pd
from fastapi import FastAPI
from starlette.testclient import TestClient

from final_project.excel2parquet import excel_2_parquet
from final_project.hash_str import hash_str
from final_project.io import atomic_write

app = FastAPI()

client = TestClient(app)

def test_try():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"hello": "world"} # WORKS


class FakeFileFailure(IOError):
    pass


class HashTests(TestCase):
    def test_basic(self):
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")
        self.assertEqual(hash_str("world!", salt="").hex()[:6], "711e96")
        self.assertEqual(hash_str("world!").hex()[:6], "711e96")
        self.assertEqual(hash_str(1, salt="hello, ").hex()[:6], "25a24b")


class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with self.assertRaises(FakeFileFailure):
                with atomic_write(fp, "w") as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure()

            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")
            with open(fp, "w"):
                pass

            with self.assertRaises(FileExistsError):
                with atomic_write(fp, "w"):
                    pass


def get_excel_data(test_data):
    test_data = {
        "hashed_id": ["hashid123", "hashid456", "hashid789"],
        "testing": ["testing1", "testing2", "testing3"],
    }
    test_df = pd.DataFrame(test_data, columns=["hashed_id", "testing"])
    return test_df


class MainTest(TestCase):

    # def test_read_excel(self):
    #     test_data = {
    #         "hashed_id": ["hashid123", "hashid456", "hashid789"],
    #         "testing": ["testing1", "testing2", "testing3"],
    #     }
    #     test_df = pd.DataFrame(test_data, columns=["hashed_id", "testing"])
    #
    #     test_out_data = io.BytesIO()
    #
    #     test_writer = pd.ExcelWriter(test_out_data)
    #     test_df.to_excel(test_writer, index=False)
    #     test_writer.save()
    #
    #     excel_data = pd.read_excel(test_out_data)
    #     pd.testing.assert_frame_equal(excel_data, test_df)

    @mock.patch("pandas.read_excel", get_excel_data)
    def test_excel_2_parquet(self):
        with TemporaryDirectory() as tempdir:
            test_excel = os.path.join(tempdir, "test_data.xslx")
            test_parquet = excel_2_parquet(test_excel)

            self.assertEqual(
                pd.read_parquet(test_parquet, columns=["hashed_id"])[
                    "hashed_id"
                ].tolist(),
                ["hashid123", "hashid456", "hashid789"],
            )
