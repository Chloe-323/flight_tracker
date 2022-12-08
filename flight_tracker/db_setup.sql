BEGIN;
--
-- Create model Airline
--
CREATE TABLE "website_airline" ("name" varchar(30) NOT NULL PRIMARY KEY);
--
-- Create model Airplane
--
CREATE TABLE "website_airplane" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "airplane_id" varchar(30) NOT NULL, "seats" integer NOT NULL, "manufacturer" varchar(30) NOT NULL, "date_built" date NOT NULL, "airline_id" varchar(30) NOT NULL REFERENCES "website_airline" ("name") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Airport
--
CREATE TABLE "website_airport" ("name" varchar(30) NOT NULL PRIMARY KEY, "city" varchar(30) NOT NULL, "country" varchar(2) NOT NULL, "airport_type" varchar(30) NOT NULL);
--
-- Create model Customer
--
CREATE TABLE "website_customer" ("email" varchar(254) NOT NULL PRIMARY KEY, "fname" varchar(30) NOT NULL, "lname" varchar(30) NOT NULL, "password_hash" varchar(256) NOT NULL, "password_salt" varchar(256) NOT NULL, "building_number" varchar(10) NOT NULL, "street" varchar(30) NOT NULL, "city" varchar(30) NOT NULL, "state" varchar(2) NOT NULL, "phone_number" varchar(10) NOT NULL, "passport_number" varchar(10) NOT NULL, "passport_expiration" date NOT NULL, "passport_country" varchar(2) NOT NULL, "date_of_birth" date NOT NULL);
--
-- Create model Flight
--
CREATE TABLE "website_flight" ("flight_number" varchar(30) NOT NULL PRIMARY KEY, "base_price" decimal NOT NULL, "departure_date" datetime NOT NULL, "arrival_date" datetime NOT NULL, "status" varchar(30) NOT NULL, "airline_id" varchar(30) NOT NULL REFERENCES "website_airline" ("name") DEFERRABLE INITIALLY DEFERRED, "airplane_id" bigint NOT NULL REFERENCES "website_airplane" ("id") DEFERRABLE INITIALLY DEFERRED, "arrival_airport_id" varchar(30) NOT NULL REFERENCES "website_airport" ("name") DEFERRABLE INITIALLY DEFERRED, "departure_airport_id" varchar(30) NOT NULL REFERENCES "website_airport" ("name") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Ticket
--
CREATE TABLE "website_ticket" ("ticket_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "sold_price" decimal NOT NULL, "card_type" varchar(30) NOT NULL, "card_number" varchar(16) NOT NULL, "expiration_date" date NOT NULL, "security_code" varchar(4) NOT NULL, "purchase_date" datetime NOT NULL, "customer_id" varchar(254) NOT NULL REFERENCES "website_customer" ("email") DEFERRABLE INITIALLY DEFERRED, "flight_id" varchar(30) NOT NULL REFERENCES "website_flight" ("flight_number") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Rating
--
CREATE TABLE "website_rating" ("rating_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rating" integer NOT NULL, "comment" varchar(1000) NOT NULL, "customer_id" varchar(254) NOT NULL REFERENCES "website_customer" ("email") DEFERRABLE INITIALLY DEFERRED, "flight_id" varchar(30) NOT NULL REFERENCES "website_flight" ("flight_number") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model AirlineStaff
--
CREATE TABLE "website_airlinestaff" ("username" varchar(30) NOT NULL PRIMARY KEY, "password_hash" varchar(256) NOT NULL, "password_salt" varchar(256) NOT NULL, "date_of_birth" date NOT NULL, "phone_number" varchar(10) NOT NULL, "email" varchar(254) NOT NULL, "airline_id" varchar(30) NOT NULL REFERENCES "website_airline" ("name") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "website_airplane_airplane_id_airline_id_e1aefebe_uniq" ON "website_airplane" ("airplane_id", "airline_id");
CREATE INDEX "website_airplane_airline_id_9d4fb249" ON "website_airplane" ("airline_id");
CREATE UNIQUE INDEX "website_flight_airline_id_flight_number_c64569f9_uniq" ON "website_flight" ("airline_id", "flight_number");
CREATE INDEX "website_flight_airline_id_75ade7fc" ON "website_flight" ("airline_id");
CREATE INDEX "website_flight_airplane_id_10293b19" ON "website_flight" ("airplane_id");
CREATE INDEX "website_flight_arrival_airport_id_7ba02655" ON "website_flight" ("arrival_airport_id");
CREATE INDEX "website_flight_departure_airport_id_105d69af" ON "website_flight" ("departure_airport_id");
CREATE INDEX "website_ticket_customer_id_4ca4dc53" ON "website_ticket" ("customer_id");
CREATE INDEX "website_ticket_flight_id_15393076" ON "website_ticket" ("flight_id");
CREATE INDEX "website_rating_customer_id_ac5279ff" ON "website_rating" ("customer_id");
CREATE INDEX "website_rating_flight_id_c11c9e22" ON "website_rating" ("flight_id");
CREATE INDEX "website_airlinestaff_airline_id_2071667f" ON "website_airlinestaff" ("airline_id");
COMMIT;

