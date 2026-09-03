-- ============================================================
-- 05_readonly_permissions.sql
-- AI Business Analyst Assistant
-- Purpose:
-- Create a dedicated PostgreSQL user for the Python AI
-- application with read-only access to the database.
-- ============================================================


-- Create the read-only login user for the application.
-- Replace the placeholder with your own password locally.
CREATE ROLE analytics_readonly
LOGIN
PASSWORD 'REPLACE_WITH_READONLY_PASSWORD';


-- Allow the read-only user to connect to the
-- AI Business Analyst database.
GRANT CONNECT
ON DATABASE ai_business_analyst
TO analytics_readonly;


-- Allow the read-only user to access the public schema.
GRANT USAGE
ON SCHEMA public
TO analytics_readonly;


-- Allow the read-only user to execute SELECT queries
-- on all existing tables in the public schema.
GRANT SELECT
ON ALL TABLES
IN SCHEMA public
TO analytics_readonly;


-- Automatically grant SELECT permission on tables
-- created in the future in the public schema.
ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT SELECT
ON TABLES
TO analytics_readonly;