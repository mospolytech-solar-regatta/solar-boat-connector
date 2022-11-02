CREATE DATABASE "solar-db";
CREATE DATABASE "solar-land";
CREATE user "solar-db" with encrypted password 'solar-db';
CREATE user "solar-land" with encrypted password 'solar-land';
ALTER DATABASE "solar-db" owner to "solar-db";
ALTER DATABASE "solar-land" owner to "solar-land";