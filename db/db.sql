drop table if exists cookie;
drop table if exists run;
drop table if exists user;

create table cookie (
  id integer primary key autoincrement,
  name varchar(255) not null,
  calories float not null,
  brand varchar(255) not null,
  website text not null
);

create table run (
  id integer primary key autoincrement,
  file_key text not null unique,
  distance float not null,
  calories float not null,
  speed float not null,
  duration float not null,
  gpx text not null,
  user_id integer null,
  added DATETIME DEFAULT CURRENT_TIMESTAMP
);

create table user (
  id integer primary key autoincrement,
  username varchar(255) not null unique,
  password_hash varchar(255) not null,
  email varchar(255) not null,
  reset_key varchar(255),
  is_admin BOOLEAN DEFAULT FALSE,
  is_banned BOOLEAN DEFAULT FALSE,
  registered DATETIME DEFAULT CURRENT_TIMESTAMP
);

insert into cookie (id, name, calories, brand, website)
values (1,'Oreo - Original',53.0,'Oreo','www.oreo.com'),
 (2,'Oreo - Chocolate Cream',51.0,'Oreo','www.oreo.com'),
 (3,'Oreo - White Choc',105.0,'Oreo','www.oreo.com'),
 (4,'Oreo - Milk Choc',105.0,'Oreo','www.oreo.com'),
 (5,'Pim''s Orange',50.0,'LU','http://www.lubiscuits.com/'),
 (6,'Pim''s Raspberry',50.0,'LU','http://www.lubiscuits.com/'),
 (7,'Dinosaurus Chocolate',95.0,'Lotus','http://www.lotusbakeries.com/'),
 (8,'Dinosaurus Milk Chocolate',94.0,'Lotus','http://www.lotusbakeries.com/'),
 (9,'Dinosaurus Grains',71.0,'Lotus','http://www.lotusbakeries.com/');

