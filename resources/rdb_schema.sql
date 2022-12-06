CREATE TABLE states (
  code varchar(255) NOT NULL,
  name varchar(255) NOT NULL,
  PRIMARY KEY (code));

CREATE TABLE counties (
  fips        SERIAL NOT NULL,
  name        varchar(255) NOT NULL,
  population  int4 NOT NULL,
  male        int4 NOT NULL,
  female      int4 NOT NULL,
  average_age float4 NOT NULL,
  latitude    float8 NOT NULL,
  longitude   float8 NOT NULL,
  state_code  varchar(255) NOT NULL,
  PRIMARY KEY (fips));

CREATE TABLE daily_cases (
  county_fips int4 NOT NULL,
  register    date NOT NULL,
  cases       int4 NOT NULL,
  deaths      int4 NOT NULL,
  male        int4 NOT NULL,
  female      int4 NOT NULL,
  PRIMARY KEY (county_fips,
  register));

ALTER TABLE counties ADD CONSTRAINT FKcounties517983 FOREIGN KEY (state_code) REFERENCES states (code);

ALTER TABLE daily_cases ADD CONSTRAINT FKdaily_case201294 FOREIGN KEY (county_fips) REFERENCES counties (fips);