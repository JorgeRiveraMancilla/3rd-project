CREATE TABLE state_dimension (
  code SERIAL NOT NULL,
  name varchar(255) NOT NULL,
  PRIMARY KEY (code));

CREATE TABLE county_dimension (
  fips       SERIAL NOT NULL,
  name       varchar(255) NOT NULL,
  male       int4 NOT NULL,
  female     int4 NOT NULL,
  latitude   float8 NOT NULL,
  longitude  float8 NOT NULL,
  state_code int4 NOT NULL,
  PRIMARY KEY (fips));

CREATE TABLE time_dimension (
  id       SERIAL NOT NULL,
  register date NOT NULL,
  year     int4 NOT NULL,
  month    int4 NOT NULL,
  day      int4 NOT NULL,
  PRIMARY KEY (id));

CREATE TABLE facts (
  id          SERIAL NOT NULL,
  male        int4 NOT NULL,
  female      int4 NOT NULL,
  deaths      int4 NOT NULL,
  county_fips int4 NOT NULL,
  time_id     int4 NOT NULL,
  PRIMARY KEY (id));

ALTER TABLE county_dimension ADD CONSTRAINT FKcounty_dim634100 FOREIGN KEY (state_code) REFERENCES state_dimension (code);

ALTER TABLE facts ADD CONSTRAINT FKfacts448904 FOREIGN KEY (county_fips) REFERENCES county_dimension (fips);

ALTER TABLE facts ADD CONSTRAINT FKfacts156297 FOREIGN KEY (time_id) REFERENCES time_dimension (id);