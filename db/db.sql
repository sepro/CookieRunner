drop table if exists cookie;
drop table if exists route;
drop table if exists user;

create table cookie (
  id integer primary key autoincrement,
  name varchar(255) not null,
  calories float not null,
  brand varchar(255) not null,
  website text not null
);

create table route (
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
  email varchar(255) not null,
  reset_key varchar(255) not null,
  registered DATETIME DEFAULT CURRENT_TIMESTAMP
);

insert into cookie (id, name, calories, brand, website)
values (1, 'Oreo', 50, 'Oreo', 'www.oreo.com');
