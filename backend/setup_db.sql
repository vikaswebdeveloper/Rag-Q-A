-- Run once: sudo -u postgres psql -f backend/setup_db.sql
CREATE ROLE rag_app LOGIN PASSWORD '<DB_PASSWORD>';
CREATE DATABASE users_db OWNER rag_app;
CREATE DATABASE userdata_db OWNER rag_app;

