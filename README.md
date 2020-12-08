# Final Project

***SQL Query Log Analysis*** 

[![Build Status](https://travis-ci.com/csci-e-29/2020fa-final-project-kumar-anish.svg?branch=master)](https://travis-ci.com/csci-e-29/2020fa-final-project-kumar-anish)

[![Maintainability](https://api.codeclimate.com/v1/badges/aaaaa/maintainability)](https://codeclimate.com/repos/aaaaa/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/aaaaa/test_coverage)](https://codeclimate.com/repos/aaaaa/test_coverage)

## Objectives

* DBA is worried about performance of database since we are adding multiple applications and database features in Teradata Vantage. 
* Some of the applications may be using SQL queries which are not optimized, and some may be using new features of machine learning which may as well impact performance. 
* It is hard to eyeball so many queries fired on database even if it is result in performance impact. 
* So, there is a need to automatically find some SQL keywords or expensive functions used in SQL and categorize them as part of recommendation for tuning. 
* Another way to look at it, if a customer is not using newly available feature of database function. 
* There may be a case when client is still using deprecated functions in SQL or not using advance features/functions of database and there is an opportunity to advise them to utilize new features for improved performance or new use case. 


### Project Scope

* Performing text analysis on relational database query/SQL logs using python library. 
* Find if there is any relation between database queries and categorize them (kind of find friends of Pset3/nearest neighbor) based on some predefined bucket of keywords/texts (expensive SQL tags/native function) sample. 
* Summarize the finding and upload the summary to database for further review as a daily report. Based on the report, DBA may act/suggest on improving (database tuning) the performance of queries by adding indexes or changing the query text or model. 
* Business may suggest client to utilize some of the new features which is not being utilized by client (no nearest neighbor). 

This problem set is designed to be solvable with minimal prep work - you should
be able to complete it with your own prior knowledge and limited external
research beyond the provided tutorials. If it proves too challenging, please
discuss with the teaching staff whether you should consider delaying enrollment
in this course.

### Technical Approach

* Export data (Database Query logs) from Teradata (relational database running in AWS) using REST API and generate file in json/parquet format.
* Perform text analytics of SQL logs in Python and produce results.
* Import the results in database. 
* Why Python: Python is largely accepted language for data science and data analysis, and it has vast library to do the same. 
It’s easy to debug and develop in local/dev environment Python  


## Project Work

### Development Artifacts: 

* Utilize Luigi for internal/external tasks scheduling. 
* Utilize atomic write to convert JSON data to PARQUET and vice versa.
* Utilize Python library (NumPy & Pandas) for text analytics of query logs. Python Classes will be utilized to Tokenize, Clean, Parse SQL Query Text.
* Utilize Word2Vec for query text categorization/nearest neighbor based on given sample. 
* Utilize REST API to export/import data from relational database (Teradata Vantage).



#### Modules of Project:

* EXPORT FROM DB USING REST API CALL /API Output:  JSON
* Atomic Write JSON to PARQUET
* SQL LOG TEXT Analytics in PYTHON Input Sample & SQL Log / Output Parquet summary
* Atomic Write PARQUET to JSON
* IMPORT DB REST API CALL: API INPUT: JSON, Output Database Table


#### Task/Process Flow of Project 




#### High Level Architecture Diagram




