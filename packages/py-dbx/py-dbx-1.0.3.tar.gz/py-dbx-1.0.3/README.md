### [doc on github.io](https://walkerever.github.io/) 


## dbx

`dbx` is the command line tool included in py-dbx package.  It was named sretools-dbx as you can see in below examples until fully updated.

 you run `dbx` or `python -mdbx` other than `sretools-dbx` in the past. 
 
 - [Installation](#installation)
 - [args](#dbx-sretools-dbx)
 - [work with db2/postgresql/mysql and more](#tests-with-db2-postgresql-and-mysql)
 - [export data](#export-to-jsonyaml-or-html)
 - [plugin](#use-plugin-for-sql-shortcut)

-----
 
 
## Installation
`pip install py-dbx`

run with `python -mdbx` or just `dbx`


## dbx (sretools-dbx) 
sretools-dbx is a generic database client using JDBC.  It's not designed to replace any current factory client but to provide people who work under terminals a new way to access their data with better console output, and ablility to export as JSON, YAML or HTML tables.  
It's at command level which means it's open to full bash access and one can always utilize his or her expertis on unix tools.

```bash
$ sretools-dbx -h
usage: sretools-dbx [-h] [-J JAR] [-u USER] [-p PASSWORD] [-D DRIVER] [-U URL] [-C] [-Q SQL] [-w MAXWIDTH] [-F FORMAT] [-v] [-X]

optional arguments:
  -h, --help            show this help message and exit
  -J JAR, --jar JAR     jdbc driver jar file
  -u USER, --user USER  user. default as current unix user.
  -p PASSWORD, --password PASSWORD
                        password. ENV["dbx_mypwd"]
  -D DRIVER, --driver DRIVER
                        jdbc driver name
  -U URL, --url URL     jdbc url or connection string
  -C, --connect         force connect as server
  -Q SQL, --sql SQL     sql statement to run
  -w MAXWIDTH, --maxwidth MAXWIDTH
                        maxwidth of column
  -F FORMAT, --outformat FORMAT
                        json,yaml,csv,html
  -v, --pivot           pivot the view
  -X, --debug           debug mode
```

## Tests with DB2, Postgresql and MySQL

###  connect to database (-C)
user/passwod can be specifed in URL/connection string. or explicitly specified. 
if not specified, dbx will try to use current unix user; as to password, it will check environment variable dbx_password then will prompt. 
in case ssl being used and not password needed, use 'dummy' for password.

```bash
$ # all in connection string
$ sretools-dbx -J ~/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U "jdbc:mysql://localhost:3306/mysql?user=yonghang&password=password&allowPublicKeyRetrieval=true&useSSL=false" -C
# DBXServer 972045@/home/yonghang/.cache/sretools/.dbx.971825
$ ps -ef | grep dbx | grep -v grep
yonghang  972045       1 21 10:24 pts/1    00:00:01 /usr/bin/python3 /usr/local/bin/sretools-dbx -J /home/yonghang/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U jdbc:mysql://localhost:3306/mysql?user=yonghang&password=password&allowPublicKeyRetrieval=true&useSSL=false -C

$ # or
$ sretools-dbx -J ~/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U "jdbc:mysql://localhost:3306/mysql?allowPublicKeyRetrieval=true&useSSL=false" -u yonghang -p password -C
# DBXServer 972146@/home/yonghang/.cache/sretools/.dbx.971825
$ ps -ef | grep dbx | grep -v grep
yonghang  972146       1 88 10:24 pts/1    00:00:01 /usr/bin/python3 /usr/local/bin/sretools-dbx -J /home/yonghang/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U jdbc:mysql://localhost:3306/mysql?allowPublicKeyRetrieval=true&useSSL=false -u yonghang -p password -C


$ # or
$ export dbx_password=password
$ sretools-dbx -J ~/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U "jdbc:mysql://localhost:3306/mysql?allowPublicKeyRetrieval=true&useSSL=false" -u yonghang -C
# DBXServer 972374@/home/yonghang/.cache/sretools/.dbx.971825
$ ps -ef | grep dbx | grep -v grep
yonghang  972374       1 32 10:25 pts/1    00:00:01 /usr/bin/python3 /usr/local/bin/sretools-dbx -J /home/yonghang/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U jdbc:mysql://localhost:3306/mysql?allowPublicKeyRetrieval=true&useSSL=false -u yonghang -C
```

###  disconnect against database 
send "\q" will cause disconnection from the database.
note, dbx can get the SQL to run with -Q or from unix pipe.
```bash
$ ps -ef | grep dbx | grep -v grep
yonghang  972374       1  0 10:25 pts/1    00:00:01 /usr/bin/python3 /usr/local/bin/sretools-dbx -J /home/yonghang/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U jdbc:mysql://localhost:3306/mysql?allowPublicKeyRetrieval=true&useSSL=false -u yonghang -C
$ sretools-dbx -Q "\q"
$ ps -ef | grep dbx | grep -v grep

$ # or
$ ps -ef | grep dbx | grep -v grep
yonghang  973586       1 89 10:31 pts/1    00:00:01 /usr/bin/python3 /usr/local/bin/sretools-dbx -J /home/yonghang/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U jdbc:mysql://localhost:3306/mysql?allowPublicKeyRetrieval=true&useSSL=false -u yonghang -C
$ echo "\q" | sretools-dbx
$ ps -ef | grep dbx | grep -v grep
$ 
```

### Query database 
use mysql as example
```bash
$ sretools-dbx -J /home/yonghang/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U 'jdbc:mysql://localhost:3306/mysql?user=yonghang&password=password&allowPublicKeyRetrieval=true&useSSL=false' -C
# DBXServer 974814@/home/yonghang/.cache/sretools/.dbx.971825
$ echo "select user,host,Select_priv,Insert_priv,Update_priv,Delete_priv,Create_priv,Create_priv,Drop_priv from mysql.user limit 2" | sretools-dbx 
user     host Select_priv Insert_priv Update_priv Delete_priv Create_priv Create_priv Drop_priv
-----------------------------------------------------------------------------------------------
root     %    Y           Y           Y           Y           Y           Y           Y
yonghang %    Y           Y           Y           Y           Y           Y           Y
$ # for very wide table, it's easier to pivot the result with -v
$ echo "select user,host,Select_priv,Insert_priv,Update_priv,Delete_priv,Create_priv,Create_priv,Drop_priv from mysql.user limit 2" | sretools-dbx  -v
user        : root
host        : %
Select_priv : Y
Insert_priv : Y
Update_priv : Y
Delete_priv : Y
Create_priv : Y
Create_priv : Y
Drop_priv   : Y
--
user        : yonghang
host        : %
Select_priv : Y
Insert_priv : Y
Update_priv : Y
Delete_priv : Y
Create_priv : Y
Create_priv : Y
Drop_priv   : Y
$ 
$ echo "select table_schema,table_name,view_definition from information_schema.views limit 2" | sretools-dbx
TABLE_SCHEMA TABLE_NAME                    VIEW_DEFINITION
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
sys          version                       select '2.1.1' AS `sys_version`,version() AS `mysql_version`
sys          innodb_buffer_stats_by_schema select if((locate('.',`ibp`.`TABLE_NAME`) = 0),'InnoDB System',replace(substring_index(`ibp`.`TABLE_NAME`,'.',1),'`','')) AS `object_schema`,format_bytes(sum(if((`ibp`.`COMPRESSED_SIZE` = 0),16384,`ibp`.`COMPRESSED_SIZE`))) AS `allocated`,format_bytes(sum(`ibp`.`DATA_SIZE`)) AS `data`,count(`ibp`.`PAGE_NUMBER`) AS `pages`,count(if((`ibp`.`IS_HASHED` = 'YES'),1,NULL)) AS `pages_hashed`,count(if((`ibp`.`IS_OLD` = 'YES'),1,NULL)) AS `pages_old`,round((sum(`ibp`.`NUMBER_RECORDS`) / count(distinct `ibp`.`INDEX_NAME`)),0) AS `rows_cached` from `information_schema`.`INNODB_BUFFER_PAGE` `ibp` where (`ibp`.`TABLE_NAME` is not null) group by `object_schema` order by sum(if((`ibp`.`COMPRESSED_SIZE` = 0),16384,`ibp`.`COMPRESSED_SIZE`)) desc
$ 
$ # limit max col width to 80 for better look
$ echo "select table_schema,table_name,view_definition from information_schema.views limit 2" | sretools-dbx -w80
TABLE_SCHEMA TABLE_NAME                    VIEW_DEFINITION
---------------------------------------------------------------------------------------------------------------------------
sys          version                       select '2.1.1' AS `sys_version`,version() AS `mysql_version`
sys          innodb_buffer_stats_by_schema select if((locate('.',`ibp`.`TABLE_NAME`) = 0),'InnoDB System',replace(substring
                                           _index(`ibp`.`TABLE_NAME`,'.',1),'`','')) AS `object_schema`,format_bytes(sum(if
                                           ((`ibp`.`COMPRESSED_SIZE` = 0),16384,`ibp`.`COMPRESSED_SIZE`))) AS `allocated`,f
                                           ormat_bytes(sum(`ibp`.`DATA_SIZE`)) AS `data`,count(`ibp`.`PAGE_NUMBER`) AS `pag
                                           es`,count(if((`ibp`.`IS_HASHED` = 'YES'),1,NULL)) AS `pages_hashed`,count(if((`i
                                           bp`.`IS_OLD` = 'YES'),1,NULL)) AS `pages_old`,round((sum(`ibp`.`NUMBER_RECORDS`)
                                   / count(distinct `ibp`.`INDEX_NAME`)),0) AS `rows_cached` from `information_sch
                                           ema`.`INNODB_BUFFER_PAGE` `ibp` where (`ibp`.`TABLE_NAME` is not null) group by
                                           `object_schema` order by sum(if((`ibp`.`COMPRESSED_SIZE` = 0),16384,`ibp`.`COMPR
                                           ESSED_SIZE`)) desc
```


in mysql, the view definition text is kind of '1 line' text which is not good for reading.  most likely we may have line breaks there.
below let's look at another example for the formatting part. the new example is with ibm-db2.

```bash
$ sretools-dbx -J /home/yonghang/jdbc/db2jcc4.jar -D com.ibm.db2.jcc.DB2Driver -U "jdbc:db2://localhost:50000/sample:user=db2inst1;password=db2inst1;" -C
# DBXServer 978653@/home/yonghang/.cache/sretools/.dbx.971825
$ 
$ echo "select viewschema,viewname,varchar(text) as text from syscat.views fetch first 1 rows only with ur" | sretools-dbx 
VIEWSCHEMA VIEWNAME          TEXT
-------------------------------------------------------------------------------------------------------
SYSIBM     CHECK_CONSTRAINTS CREATE OR REPLACE VIEW SYSIBM.CHECK_CONSTRAINTS
                             (CONSTRAINT_CATALOG, CONSTRAINT_SCHEMA, CONSTRAINT_NAME, CHECK_CLAUSE)
                             AS SELECT
                             CAST(CURRENT SERVER AS VARCHAR(128)), TBCREATOR,
                             CAST(NAME AS VARCHAR(128)), TEXT
                             FROM SYSIBM.SYSCHECKS
                             WHERE TYPE='C'
                             UNION ALL
                             SELECT CAST(CURRENT SERVER AS VARCHAR(128)), TBCREATOR,
                             CAST(CONCAT(RTRIM(CONCAT(CHAR(CTIME), CHAR(FID) ) ),
                             RTRIM(CHAR(COLNO)) ) AS VARCHAR(128) ),
                             CAST(CONCAT(CONCAT('CHECK (', C.NAME), ' IS NOT NULL)') AS CLOB(64K) )
                             FROM SYSIBM.SYSCOLUMNS C, SYSIBM.SYSTABLES T
                             WHERE C.TBCREATOR = T.CREATOR AND C.TBNAME = T.NAME AND TYPE IN('U', 'T')
                             AND NULLS ='N'

```
## export to JSON,YAML or HTML
```bash
$ echo "select viewschema,viewname,varchar(text) as text from syscat.views fetch first 1 rows only with ur" | sretools-dbx  -Fjson
[
  {
    "VIEWSCHEMA": "SYSIBM  ",
    "VIEWNAME": "CHECK_CONSTRAINTS",
    "TEXT": "CREATE OR REPLACE VIEW SYSIBM.CHECK_CONSTRAINTS \n(CONSTRAINT_CATALOG, CONSTRAINT_SCHEMA, CONSTRAINT_NAME, CHECK_CLAUSE) \nAS SELECT \nCAST(CURRENT SERVER AS VARCHAR(128)), TBCREATOR, \nCAST(NAME AS VARCHAR(128)), TEXT \nFROM SYSIBM.SYSCHECKS \nWHERE TYPE='C' \nUNION ALL \nSELECT CAST(CURRENT SERVER AS VARCHAR(128)), TBCREATOR, \nCAST(CONCAT(RTRIM(CONCAT(CHAR(CTIME), CHAR(FID) ) ), \nRTRIM(CHAR(COLNO)) ) AS VARCHAR(128) ), \nCAST(CONCAT(CONCAT('CHECK (', C.NAME), ' IS NOT NULL)') AS CLOB(64K) ) \nFROM SYSIBM.SYSCOLUMNS C, SYSIBM.SYSTABLES T \nWHERE C.TBCREATOR = T.CREATOR AND C.TBNAME = T.NAME AND TYPE IN('U', 'T') \nAND NULLS ='N'\n"
  }
] 
$ echo "select viewschema,viewname,varchar(text) as text from syscat.views fetch first 1 rows only with ur" | sretools-dbx  -Fyaml
- TEXT: "CREATE OR REPLACE VIEW SYSIBM.CHECK_CONSTRAINTS \n(CONSTRAINT_CATALOG, CONSTRAINT_SCHEMA,\
    \ CONSTRAINT_NAME, CHECK_CLAUSE) \nAS SELECT \nCAST(CURRENT SERVER AS VARCHAR(128)),\
    \ TBCREATOR, \nCAST(NAME AS VARCHAR(128)), TEXT \nFROM SYSIBM.SYSCHECKS \nWHERE\
    \ TYPE='C' \nUNION ALL \nSELECT CAST(CURRENT SERVER AS VARCHAR(128)), TBCREATOR,\
    \ \nCAST(CONCAT(RTRIM(CONCAT(CHAR(CTIME), CHAR(FID) ) ), \nRTRIM(CHAR(COLNO))\
    \ ) AS VARCHAR(128) ), \nCAST(CONCAT(CONCAT('CHECK (', C.NAME), ' IS NOT NULL)')\
    \ AS CLOB(64K) ) \nFROM SYSIBM.SYSCOLUMNS C, SYSIBM.SYSTABLES T \nWHERE C.TBCREATOR\
    \ = T.CREATOR AND C.TBNAME = T.NAME AND TYPE IN('U', 'T') \nAND NULLS ='N'\n"
  VIEWNAME: CHECK_CONSTRAINTS
  VIEWSCHEMA: 'SYSIBM  '
$ 
$ 
$ echo "select viewschema,viewname,varchar(text) as text from syscat.views fetch first 1 rows only with ur" | sretools-dbx  -Fhtml
<table border=1 style="border-collapse:collapse;">
<tr>
<td><b>VIEWSCHEMA</b></td>
<td><b>VIEWNAME</b></td>
<td><b>TEXT</b></td>
</tr>
<tr>
<td>SYSIBM  </td>
<td>CHECK_CONSTRAINTS</td>
<td>CREATE OR REPLACE VIEW SYSIBM.CHECK_CONSTRAINTS <br>(CONSTRAINT_CATALOG, CONSTRAINT_SCHEMA, CONSTRAINT_NAME, CHECK_CLAUSE) <br>AS SELECT <br>CAST(CURRENT SERVER AS VARCHAR(128)), TBCREATOR, <br>CAST(NAME AS VARCHAR(128)), TEXT <br>FROM SYSIBM.SYSCHECKS <br>WHERE TYPE='C' <br>UNION ALL <br>SELECT CAST(CURRENT SERVER AS VARCHAR(128)), TBCREATOR, <br>CAST(CONCAT(RTRIM(CONCAT(CHAR(CTIME), CHAR(FID) ) ), <br>RTRIM(CHAR(COLNO)) ) AS VARCHAR(128) ), <br>CAST(CONCAT(CONCAT('CHECK (', C.NAME), ' IS NOT NULL)') AS CLOB(64K) ) <br>FROM SYSIBM.SYSCOLUMNS C, SYSIBM.SYSTABLES T <br>WHERE C.TBCREATOR = T.CREATOR AND C.TBNAME = T.NAME AND TYPE IN('U', 'T') <br>AND NULLS ='N'<br></td>
</tr>
```

## use plugin for sql shortcut
plugin is YAML file including queries.  I made a random example from some SQL from internet as below.

generated YAML file,
```yaml
mysql:
  db:
    usage: '

      SELECT s.schema_name,

      CONCAT(IFNULL(ROUND((SUM(t.data_length)+SUM(t.index_length))/1024/1024,2),0.00),"Mb")
      total_size,

      CONCAT(IFNULL(ROUND(((SUM(t.data_length)+SUM(t.index_length))-SUM(t.data_free))/1024/1024,2),0.00),"Mb")
      data_used,

      CONCAT(IFNULL(ROUND(SUM(data_free)/1024/1024,2),0.00),"Mb") data_free,

      IFNULL(ROUND((((SUM(t.data_length)+SUM(t.index_length))-SUM(t.data_free))/((SUM(t.data_length)+SUM(t.index_length)))*100),2),0)
      pct_used

      FROM INFORMATION_SCHEMA.SCHEMATA s, INFORMATION_SCHEMA.TABLES t

      WHERE s.schema_name = t.table_schema

      GROUP BY s.schema_name

      ORDER BY total_size DESC

      '
  perf: {}
  tablespace:
    usage: '

      SELECT s.schema_name, table_name,

      CONCAT(IFNULL(ROUND((SUM(t.data_length)+SUM(t.index_length))/1024/1024,2),0.00),"Mb")
      total_size,

      CONCAT(IFNULL(ROUND(((SUM(t.data_length)+SUM(t.index_length))-SUM(t.data_free))/1024/1024,2),0.00),"Mb")
      data_used,

      CONCAT(IFNULL(ROUND(SUM(data_free)/1024/1024,2),0.00),"Mb") data_free,

      IFNULL(ROUND((((SUM(t.data_length)+SUM(t.index_length))-SUM(t.data_free))/((SUM(t.data_length)+SUM(t.index_length)))*100),2),0)
      pct_used

      FROM INFORMATION_SCHEMA.SCHEMATA s, INFORMATION_SCHEMA.TABLES t

      WHERE s.schema_name = t.table_schema

      GROUP BY s.schema_name, table_name

      ORDER BY total_size DESC

      '
  user: select user,host from mysql.user
```

then load the YAML plugin with -P. This can be loaded when starting the connection then all following connections can use the commands defined.  Or you can specify the plugin for each run -- this also means you can use differnt plugins.

```bash

$ sretools-dbx  -J ~/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U "jdbc:mysql://localhost:3306/mysql?user=yonghang&password=password&allowPublicK
eyRetrieval=true&useSSL=false" -C
# DBXServer 1071685@/home/yonghang/.cache/sretools/.dbx.1065306
$ echo "\mysql.user" | ./dbx.py   -P test/test.plugin.yaml
user             host
--------------------------
root             %
yonghang         %
mysql.infoschema localhost
mysql.session    localhost
mysql.sys        localhost
root             localhost
$ sretools-dbx  -P test/test.plugin.yaml  -J ~/jdbc/mariadb-java-client-2.7.1.jar -D org.mariadb.jdbc.Driver -U "jdbc:mysql://localhost:3306/mysql?user=yonghang&pass
word=password&allowPublicKeyRetrieval=true&useSSL=false" -C
# DBXServer 1071773@/home/yonghang/.cache/sretools/.dbx.1065306
$ 
$ echo "\mysql.user" | ./dbx.py  
user             host
--------------------------
root             %
yonghang         %
mysql.infoschema localhost
mysql.session    localhost
mysql.sys        localhost
root             localhost
$ 
$ echo "\mysql.db.usage" | ./dbx.py  
SCHEMA_NAME        total_size data_used data_free pct_used
----------------------------------------------------------
mysql              7.70Mb     -120.30Mb 128.00Mb  -1561.66
sys                0.02Mb     0.02Mb    0.00Mb    100.0
sample             0.02Mb     0.02Mb    0.00Mb    100.0
information_schema 0.00Mb     0.00Mb    0.00Mb    0.0
performance_schema 0.00Mb     0.00Mb    0.00Mb    0.0
$ 
$ echo "\mysql.tablespace.usage" | ./dbx.py  
SCHEMA_NAME        TABLE_NAME                                           total_size data_used data_free pct_used
---------------------------------------------------------------------------------------------------------------
mysql              time_zone_transition                                 4.52Mb     0.52Mb    4.00Mb    11.42
mysql              help_topic                                           1.61Mb     -2.39Mb   4.00Mb    -148.54
mysql              time_zone_transition_type                            0.44Mb     -3.56Mb   4.00Mb    -814.29
mysql              time_zone_name                                       0.25Mb     -3.75Mb   4.00Mb    -1500.0
mysql              help_keyword                                         0.23Mb     -3.77Mb   4.00Mb    -1606.67
mysql              help_relation                                        0.08Mb     -3.92Mb   4.00Mb    -5020.0
mysql              time_zone                                            0.08Mb     -3.92Mb   4.00Mb    -5020.0
mysql              global_grants                                        0.05Mb     -3.95Mb   4.00Mb    -8433.33
mysql              db                                                   0.03Mb     -3.97Mb   4.00Mb    -12700.0
mysql              help_category                                        0.03Mb     -3.97Mb   4.00Mb    -12700.0
mysql              procs_priv                                           0.03Mb     -3.97Mb   4.00Mb    -12700.0
mysql              proxies_priv                                         0.03Mb     -3.97Mb   4.00Mb    -12700.0
mysql              tables_priv                                          0.03Mb     -3.97Mb   4.00Mb    -12700.0
mysql              columns_priv                                         0.02Mb     -3.98Mb   4.00Mb    -25500.0
mysql              component                                            0.02Mb     -3.98Mb   4.00Mb    -25500.0
mysql              default_roles                                        0.02Mb     -3.98Mb   4.00Mb    -25500.0
mysql              engine_cost                                          0.02Mb     -3.98Mb   4.00Mb    -25500.0
mysql              func                                                 0.02Mb     -3.98Mb   4.00Mb    -25500.0
mysql              gtid_executed                                        0.02Mb     -3.98Mb   4.00Mb    -25500.0
mysql              innodb_index_stats                                   0.02Mb     -3.98Mb   4.00Mb    -25500.0
mysql              innodb_table_stats                                   0.02Mb     -3.98Mb   4.00Mb    -25500.0
mysql              password_history                                     0.02Mb     -3.98Mb   4.00Mb    -25500.0
......
performance_schema session_connect_attrs                                0.00Mb     0.00Mb    0.00Mb    0.0
performance_schema session_status                                       0.00Mb     0.00Mb    0.00Mb    0.0
performance_schema session_variables                                    0.00Mb     0.00Mb    0.00Mb    0.0
performance_schema setup_actors                                         0.00Mb     0.00Mb    0.00Mb    0.0
performance_schema setup_consumers                                      0.00Mb     0.00Mb    0.00Mb    0.0
$ 
```









