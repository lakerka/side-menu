CREATE USER products_app_user WITH PASSWORD 'strongpassword';
ALTER ROLE products_app_user SET client_encoding TO 'utf8';
ALTER ROLE products_app_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE products_app_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE products TO products_app_user;

CREATE DATABASE products;
-- while connected to products database
CREATE EXTENSION IF NOT EXISTS ltree;
