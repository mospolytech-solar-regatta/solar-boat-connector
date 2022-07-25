CREATE DATABASE "solar-boat";
CREATE DATABASE "solar-api";
CREATE user "solar-boat" with encrypted password 'solar-boat';
CREATE user "solar-api" with encrypted password 'solar-api';
ALTER DATABASE "solar-boat" owner to "solar-boat";
ALTER DATABASE "solar-api" owner to "solar-api";