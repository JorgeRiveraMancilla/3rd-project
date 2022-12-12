DROP TABLE IF EXISTS county_dimension CASCADE;
DROP TABLE IF EXISTS facts CASCADE;
DROP TABLE IF EXISTS time_dimension CASCADE;
DROP TABLE IF EXISTS state_dimension CASCADE;

CREATE TABLE county_dimension
(
    fips              SERIAL       NOT NULL,
    name              varchar(255) NOT NULL,
    male_population   int4         NOT NULL,
    female_population int4         NOT NULL,
    total_population  int4         NOT NULL,
    latitude          float8       NOT NULL,
    longitude         float8       NOT NULL,
    state_code        varchar(255) NOT NULL,
    PRIMARY KEY (fips)
);



CREATE TABLE facts
(
    id           SERIAL NOT NULL,
    male_cases   int4   NOT NULL,
    female_cases int4   NOT NULL,
    total_cases  int4   NOT NULL,
    deaths       int4   NOT NULL,
    county_fips  int4   NOT NULL,
    time_id      int4   NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE time_dimension
(
    id       SERIAL NOT NULL,
    register date   NOT NULL UNIQUE,
    year     int4   NOT NULL,
    month    int4   NOT NULL,
    day      int4   NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE state_dimension
(
    code varchar(255) NOT NULL,
    name varchar(255) NOT NULL UNIQUE,
    PRIMARY KEY (code)
);


ALTER TABLE county_dimension
    ADD CONSTRAINT FKcounty_dim634100 FOREIGN KEY (state_code) REFERENCES state_dimension (code);


ALTER TABLE facts
    ADD CONSTRAINT FKfacts448904 FOREIGN KEY (county_fips) REFERENCES county_dimension (fips);

ALTER TABLE facts
    ADD CONSTRAINT FKfacts156297 FOREIGN KEY (time_id) REFERENCES time_dimension (id);

