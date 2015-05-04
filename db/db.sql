drop table if exists cookie;
drop table if exists gpx;
drop table if exists users;

create table cookie (
  id integer primary key autoincrement,
  name varchar(255) not null,
  calories float not null,
  brand varchar(255) not null,
  website text not null
);

create table gpx (
  id integer primary key autoincrement,
  file_key varchar(255) not null unique,
  distance float not null,
  calories float not null,
  speed float not null,
  gpx text not null,
  user_id integer not null,
  added DATETIME DEFAULT CURRENT_TIMESTAMP
);

create table users (
  id integer primary key autoincrement,
  username varchar(255) not null unique,
  email varchar(255) not null,
  reset_key varchar(255) not null,
  registered DATETIME DEFAULT CURRENT_TIMESTAMP
);

insert into cookie (id, name, calories, brand, website)
values (1, 'Oreo', 50, 'Oreo', 'www.oreo.com');
