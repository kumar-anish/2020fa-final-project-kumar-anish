# Final Project

***SQL Query Log Analysis*** 

[![Build Status](https://travis-ci.com/csci-e-29/2020fa-final-project-kumar-anish.svg?branch=master)](https://travis-ci.com/csci-e-29/2020fa-final-project-kumar-anish)

[![Maintainability](https://api.codeclimate.com/v1/badges/aaaaa/maintainability)](https://codeclimate.com/repos/aaaaa/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/aaaaa/test_coverage)](https://codeclimate.com/repos/aaaaa/test_coverage)

## SQL Query Log Analysis

A CSCI E-29 Final Project that uses Teradata database SQL logs for text analytics using Word2Vec.
 Some details about the background is given below:
* DBA is worried about performance of database since we are adding multiple applications and database features in Teradata Vantage. 
* Some of the applications may be using SQL queries which are not optimized, 
and some may be using new features of machine learning which may as well impact performance. 
* It is hard to eyeball so many queries fired on database even if it is result in performance impact the perfornance of databse. 
So, there is a need to automatically find/search specific SQL keywords or SQL functions (Which can potentially cause performance issue) 
used in SQL Logs and categorize/score them as part of recommendation for tuning. 
* Another way to look at it, if a customer is not using newly available feature of database. 
There may be a case when client is still using deprecated functions in SQL or not using advance features/functions of database and 
there is an opportunity to advise them to utilize new features for improved performance or new use case. 


### Project Scope

* Performing text analysis on relational database (Teradata) query/SQL logs using python library. 
* Find if there is any relation between database queries and categorize them (kind of find/match friends of Pset3/nearest neighbor) based on some predefined bucket of keywords/texts (expensive SQL tags/native function) sample. 
* Summarize/Score the finding of SQL Query Log and upload the summary to Teradata database for further review as a daily report. Based on the uploaded data in report or Dashboard, 
DBA may act/suggest on improving (database tuning) the performance of queries by adding indexes or changing the query text or model or suggesting the team who are responsible for management. 
* Business may suggest client to utilize some of the new features which is not being utilized by client (no nearest neighbor). 


### Technical Approach

* Export data (Database Query logs) from Teradata (relational database running in AWS (production) or VM (local/dev)) using REST API 
and export SQL Logs file in json.
* Perform text analytics(Word2Vec) of SQL logs in Python and produce results as csv file.
* Import the csv results in Teradata database. 
* Why Python: Python is largely accepted language for data science and data analysis, and it has vast library to do the same. 
It’s easy to debug and develop in local/dev environment Python. Database is not rich in text analytics functions/feature. 


## Project Work

### Development Task: 
* Utilize FastAPI to connect to Teradata dabase and export SQL Query Logs using rest api call. 
* Utilize Luigi for integrate with FastAPI and produce JSON file so that it can be scheduled. 
* Utilize python library json2parquet to convert JSON data to PARQUET so that it can be used in Word2Vec process.
* Download data from AWS (words.txt and numpy vector - reuse modified Pset 3 code for this and below 2 steps)
* Utilize Python library (NumPy & Pandas) for text analytics of exported query logs in parquet. 
Python Classes will be utilized to Tokenize, Clean, Parse SQL Query Text.SQL keyword or function name match is specified as 
environment variable (MY_SQL_QUERY_MATCH_TEXT)
* Utilize Word2Vec for query text categorization/nearest top 3 match based on given environment variable. 
* Export match result to csv
* Utilize sqlalchemy to import csv data to relational database (Teradata ).



#### Python Module Details:

* api.py 
(FastAPI/ uvicorn implementation) EXPORT FROM DB USING REST API CALL /API Output:  JSON 
HTTP GET REQUEST is /querylog/ which execute query to fetch top 100 recent database query logs
Below is the Query details

SELECT TOP 100 QueryId, QueryText
FROM dbc.qrylog
ORDER BY collecttimestamp desc

* fastapi_client.py Use for testing the rest service
* tasks.py Luigi task which calls rest api and gives output of JSON file. /data/query_logs.json
* json2parq.py Converts JSON to PARQUET 
* excel2parq.py Converts Excel to PARQUET 
* data.py loads Numpy array and words.txt along with SQL Query Text parquet file (Code Reuse)
* cli.py SQL LOG TEXT Analytics (Word2Vec) in PYTHON Input Numpy array, Words.txt & SQL Log / Output CSV summary (Code Modified)
* embedding.py (Code reuse by cli.py)
* database.py  sqlalchemy database session management ( using env variable DB_CONN)
* models.py sqlalchemy model for database table insert 
* load.py  Write CSV result summary to Teradata database (QUERYRESULT table)

Note: json2parq module was giving  error and due to time constants, data conversion was done using excel2parq. 
      excel was downloaded by running SQL query on Teradata Studio.


## Installation
1. You need recent version of Python (>=3.7)
2. Teradata Database ( for dev it can be running locally on a VM, e.g. VMWare Fusion) 
   You can configure Teradata database in AWS cloud for production. For final project, this has 
   been tested on Teradata VM running locally.
   You can download teradata database from downloads.teradata.com. You need to enable Query logging for database user.
3. Create a table in database to store summary results (Script is given below)
CREATE SET TABLE QUERYRESULT ,NO FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO
     (
      QUERYID VARCHAR(100) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
      MATCHSCORE VARCHAR(100) CHARACTER SET LATIN NOT CASESPECIFIC,
CONSTRAINT MST_QUERYRESULT_PK PRIMARY KEY ( QUERYID ));
3. Copy this repository (Clone or Copy)
4. Define ENV variables (.env)
CSCI_SALT=XXXXXXXXXXXXXXXXXXXXXXXXX
AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXX
CI_USER_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXX
MY_SQL_QUERY_MATCH_TEXT=NULLIFZERO SUM AVG TRIM FunctionName
DB_CONN=teradatasql://usr1:pwd1@192.168.1.150
5. For FastAPI, define tdconn.json at root level of project, sample content is below
{"host": "192.168.1.150", "password": "pwd1", "user": "usr1"}

 
##  Running the Application
Assumption: Teradata is already running locally (dev) or in AWS (production) and constains query logs of users in DBC tables.

### 1. Run below commands for install and path setup
* pipenv install --dev
* pipenv shell 

### 2. Start Uvicorn server by running below command
* python final_project/api.py 

Note: it will started on the console with the below statements on console. 
You may test the welcome URL and rest api call from browser

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13900] using statreload
INFO:     Started server process [13904]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

### 3. Open a new terminal and run below command to export sql to json file using luigi
* python run_luigi.py

below is sample console output of luigi task:

DEBUG: Checking if SQLLogsToJSON() is complete

INFO: Informed scheduler that task   SQLLogsToJSON__99914b932b   has status   PENDING

INFO: Done scheduling tasks

INFO: Running Worker with 1 processes

DEBUG: Asking scheduler for work...

DEBUG: Pending tasks: 1

INFO: [pid 14205] Worker Worker(salt=242203623, workers=1, host=ak-imac.local, username=ka, pid=14205) running   SQLLogsToJSON()

INFO: [pid 14205] Worker Worker(salt=242203623, workers=1, host=ak-imac.local, username=ka, pid=14205) done      SQLLogsToJSON()

DEBUG: 1 running tasks, waiting for next task to finish

INFO: Informed scheduler that task   SQLLogsToJSON__99914b932b   has status   DONE

DEBUG: Asking scheduler for work...

DEBUG: Done

DEBUG: There are no more tasks to run at this time

INFO: Worker Worker(salt=242203623, workers=1, host=ak-imac.local, username=ka, pid=14205) was stopped. Shutting down Keep-Alive thread

INFO: 

===== Luigi Execution Summary =====

Scheduled 1 tasks of which:
* 1 ran successfully:
    - 1 SQLLogsToJSON()

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====



### 4. Run below python for text analyse using word2vec and product summary csv file
* python cli.py

it will product "query_result_file.csv" along with top 3 SQL Log matched with keyword
Below is the sample console output for my local environment.


my_matched_sql_keywords_text:

NULLIFZERO SUM AVG TRIM FunctionName


top 3 matched with high scores / shorted distance sql texts: 

id          : 17
distance    : 0.42183470726013184
QueryText text:
SELECT FunctionName, TRIM(Fcns.FunctionType) AS FunctionType, TRIM(Fcns.SrcFileLanguage) AS SrcFileLanguage, TRIM(Fcns.DeterministicOpt) AS DeterministicOpt, TRIM(Fcns.ExternalName) AS ExternalName, Fcns.ExtFileReference, TRIM(Fcns.NullCall) AS NullCall, TRIM(Fcns.SpecificName) AS SpecificName, TRIM(Fcns.ParameterStyle) AS ParameterStyle, TRIM (Tbls.CommentString) AS CommentString FROM DBC.FunctionsV Fcns ,DBC.TablesV Tbls WHERE Fcns.DatabaseName = ? AND Fcns.RoutineKind = 'R'  AND Fcns.SpecificName = Tbls.TableName AND Fcns.DatabaseName = Tbls.DatabaseName


id          : 16
distance    : 0.42183470726013184
QueryText text:
SELECT FunctionName, TRIM(Fcns.FunctionType) AS FunctionType, TRIM(Fcns.SrcFileLanguage) AS SrcFileLanguage, TRIM(Fcns.DeterministicOpt) AS DeterministicOpt, TRIM(Fcns.ExternalName) AS ExternalName, Fcns.ExtFileReference, TRIM(Fcns.NullCall) AS NullCall, TRIM(Fcns.SpecificName) AS SpecificName, TRIM(Fcns.ParameterStyle) AS ParameterStyle, TRIM (Tbls.CommentString) AS CommentString FROM DBC.FunctionsV Fcns ,DBC.TablesV Tbls WHERE Fcns.DatabaseName = ? AND Fcns.RoutineKind = 'R'  AND Fcns.SpecificName = Tbls.TableName AND Fcns.DatabaseName = Tbls.DatabaseName


id          : 31
distance    : 0.4315459132194519
QueryText text:
LOCK DBC.TableSizeV FOR ACCESS SELECT TableName, SUM(CurrentPerm) AS CurrentPerm, SUM(PeakPerm) AS PeakPerm, (100 - (AVG(CurrentPerm)/NULLIFZERO(MAX(CurrentPerm))*100)) AS SkewFactor FROM DBC.TableSizeV WHERE DataBaseName = ? GROUP BY TableName ORDER BY TableName




### 5. Run below python file to upload the results to database (Tablename QUERYRESULT).
* python load.py

This will upload/insert cvs file to Teradata database table. You will see below statements on console:

loading csv results to database - start...

loading csv results to database - done...




