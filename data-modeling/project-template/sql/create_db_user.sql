

-- 
-- Create user student with permission to create database 
--
CREATE USER student WITH CREATEDB PASSWORD 'student';

-- 
-- Create default database for student user
--
CREATE DATABASE studentdb OWNER student ENCODING 'utf8' TEMPLATE template0;
