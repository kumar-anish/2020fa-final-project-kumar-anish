from pathlib import Path
from typing import List, Any, Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic.dataclasses import dataclass
from teradatasql import connect
import uvicorn


@dataclass
class SqlQueryLog:
    QueryID: str
    QueryText: str


sess = connect(Path("tdconn.json").read_text())
app = FastAPI(title="api", description="Final Project REST API Application")

teradata_querylog_sql = """\
SELECT TOP 100 QueryId
	, QueryText
FROM dbc.qrylog
ORDER BY collecttimestamp desc"""


def runsql(sql: str) -> List[List[Any]]:
    "run a sql query and return results"
    with sess.cursor() as csr:
        print(sql)
        csr.execute(sql)
        return csr.fetchall()


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    "Welcome page"
    return """\
		<h1>Welcome to Final Project</h1>
		<p>This is a sample Python application that uses Teradata database to fetch query logs to users via REST API</p>
		"""


@app.get("/querylog/")
def querylog_list() -> List[SqlQueryLog]:
    "return a list of QueryId and QueryText"
    return [SqlQueryLog(*row) for row in runsql(teradata_querylog_sql)]



if __name__ == "__main__":
    uvicorn.run("api:app", host='127.0.0.1', port=8000, reload=True)
