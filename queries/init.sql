-- creates the user, database and pg_stat_statements
CREATE USER elog WITH PASSWORD 'bbaeelog2bdf';
CREATE DATABASE elog OWNER elog;
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
