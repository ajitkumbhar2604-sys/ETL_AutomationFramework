# Project -> taf_jan_march_2026
### 1. Create new project
### 2. Settings-> project structure->Add content Root
        2.1 Selet spark-3.4.2-bib-hadoop3 -> select python
        2.2 again add python-> lib-> py4j-0.10-9.7.src
### 3. Create project folder structure/ Hierarchey 
        3.1 taf_jan_march_2026 -> python package -> src
        3.2 src -> package -> data_validations
        3.3 src -> package -> utility
        3.4 taf_jan_march_2026 -> python package -> tests
        3.5 tests -> directory -> table1
            3.5.1 table1-> config.yml
            3.5.2 table1-> schema.json
            3.5.3 table1-> transformation.sql
            3.5.4 table1-> test_table1.py
        3.6 copy table1 and paste make table2
        3.7 tests -> py file -> conftest.py
        3.8 tests -> file -> pytest.ini
        3.9 tests -> py file -> runner.py
        3.10 tests -> file -> requirements.txt
        3.11 taf_jan_march_2026 -> file -> readme.md

=========================================================================================
To read data from source and target we need below steps:
to full fill the 1st def test_count() Testcase,
### We need the data from Source and Target 
Step1: Source data, Target data
    1.1 Read Source Data (to perform below create functions for Read source and target )
        1.1.1 File data (May your source in any file format like CSV, JSON,XML,XlSX, Bin)
            Path, delimiter, header, schema, file_type
            Access Kay/role (If file is present on ADLS/S3/GCP)
        1.1.2 Database( Source is any db)
            Database credentials, host, server, port, query/table, jars
        1.1.3 Stream (data is on live stream like Kafka)
            Stream server, topic 
    1.2 Read Target Data
        1.2.1 File data (May your Target in any file format like CSV, JSON,XML,XlSX, Bin)
            Path, delimiter, header, schema, file_type
            Access Kay/role (If file is present on ADLS/S3/GCP)
        1.2.2 Database( Target is any db)
            Database credentials, host, server, port, query/table, jars
        1.2.3 Stream (data is on live stream like Kafka)
            Stream server, topic
Step2: Validations
        2.1 Count, Duplicate, Null, ....Data Quality checks
Step3: Reporting
============================================================================================

=> Create read_data as fixture, and place it inside conftest.py file(#Fixture File#), Pass it to def test_count() (as common function)
=> conftest -> add read_data function 
=> Add another fixture in conftest as read_config()
=> Add def read_sql() to read query from sql file 
=> Add def read_schema() to read schema from json file 
=> Add def spark_session() to create spark session, scope = session
required only when, 
read_sql() -> Only when source/target is database
read_schema() -> when source/targte is file
So mark them as Function only, Not Fixture 
==========================================================================================
=> Now add code for spark_session()
