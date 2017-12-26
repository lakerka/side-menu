-- these commands should be run as postgres user


CREATE USER products_app_user WITH CREATEDB PASSWORD 'strongpassword';
ALTER ROLE products_app_user SET client_encoding TO 'utf8';
ALTER ROLE products_app_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE products_app_user SET timezone TO 'UTC';


CREATE DATABASE products;
-- while connected to products db
CREATE EXTENSION IF NOT EXISTS ltree;

CREATE DATABASE test_products;
-- while connected to test_products db
CREATE EXTENSION IF NOT EXISTS ltree;
