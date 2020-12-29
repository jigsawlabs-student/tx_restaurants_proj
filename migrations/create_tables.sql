DROP TABLE IF EXISTS retailers;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS zipcodes;
DROP TABLE IF EXISTS cities_zips;

CREATE TABLE IF NOT EXISTS cities (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS zipcodes (
  zip INTEGER PRIMARY KEY
  -- more to go here later
);

CREATE TABLE IF NOT EXISTS retailers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  zip_id INT,
  city_id INT,
  liquor_sales INT,
  beer_sales INT,
  wine_sales INT,
  cover_sales INT,
  CONSTRAINT fk_zip
      FOREIGN KEY(zip_id) 
      REFERENCES zipcodes(zip)
      ON DELETE CASCADE,
  CONSTRAINT fk_city
      FOREIGN KEY(city_id) 
      REFERENCES cities(id)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cities_zipcodes (
  id SERIAL PRIMARY KEY,
  city_id INT,
  zip_id INT,
  UNIQUE (city_id, zip_id),
  CONSTRAINT fk_city
      FOREIGN KEY(city_id) 
      REFERENCES cities(id)
      ON DELETE CASCADE,
  CONSTRAINT fk_zip
      FOREIGN KEY(zip_id) 
      REFERENCES zipcodes(zip)
      ON DELETE CASCADE
);


