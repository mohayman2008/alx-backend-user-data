-- load into server using 'cat load_user_csv.sql | mysql --local-infile=1'
SET GLOBAL local_infile=1;

USE my_db;

LOAD DATA LOCAL INFILE './user_data.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
