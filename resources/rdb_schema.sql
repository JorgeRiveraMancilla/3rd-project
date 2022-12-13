DROP TABLE IF EXISTS states CASCADE;
DROP TABLE IF EXISTS daily_cases CASCADE;
DROP TABLE IF EXISTS counties CASCADE;

CREATE TABLE states
(
    code varchar(255) NOT NULL,
    name varchar(255) NOT NULL UNIQUE,
    PRIMARY KEY (code)
);

CREATE TABLE daily_cases
(
    county_fips  int4 NOT NULL,
    register     date NOT NULL,
    male_cases   int4 NOT NULL,
    female_cases int4 NOT NULL,
    deaths       int4 NOT NULL,
    PRIMARY KEY (county_fips, register)
);

CREATE TABLE counties
(
    fips              SERIAL       NOT NULL,
    name              varchar(255) NOT NULL,
    male_population   int4         NOT NULL,
    female_population int4         NOT NULL,
    average_age       float4       NOT NULL,
    latitude          float8       NOT NULL,
    longitude         float8       NOT NULL,
    state_code        varchar(255) NOT NULL,
    PRIMARY KEY (fips)
);

ALTER TABLE counties
    ADD CONSTRAINT FKcounties517983 FOREIGN KEY (state_code) REFERENCES states (code);

ALTER TABLE daily_cases
    ADD CONSTRAINT FKdaily_case201294 FOREIGN KEY (county_fips) REFERENCES counties (fips);
