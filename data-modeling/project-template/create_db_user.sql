
-- 
-- Create default database 
--
CREATE DATABASE studentdb;

BEGIN;
-- 
-- Create user student with permission to create database 
--
CREATE USER student WITH CREATEDB PASSWORD 'student';

-- 
-- Grant all permissions to student user on studentdb database 
--
GRANT ALL PRIVILEGES ON DATABASE studentdb TO student;

COMMIT;
