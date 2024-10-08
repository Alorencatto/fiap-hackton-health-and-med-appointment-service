-- Appointment Service Database
CREATE DATABASE "appointment";
CREATE USER appointment_app WITH PASSWORD '123abc';
GRANT ALL PRIVILEGES ON DATABASE "appointment" TO appointment_app;

\c appointment
GRANT ALL PRIVILEGES ON SCHEMA public TO appointment_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO appointment_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO appointment_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO appointment_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO appointment_app;

-- Keycloak Database
CREATE DATABASE "keycloak_db";
CREATE USER keycloak WITH PASSWORD 'keycloakpassword';
GRANT ALL PRIVILEGES ON DATABASE "keycloak_db" TO keycloak;

\c keycloak_db
GRANT ALL PRIVILEGES ON SCHEMA public TO keycloak;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO keycloak;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO keycloak;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO keycloak;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO keycloak;

-- Kong Database
CREATE DATABASE "kong_db";
CREATE USER kong WITH PASSWORD 'kongpassword';
GRANT ALL PRIVILEGES ON DATABASE "kong_db" TO kong;

\c kong_db
GRANT ALL PRIVILEGES ON SCHEMA public TO kong;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO kong;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO kong;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO kong;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO kong;
