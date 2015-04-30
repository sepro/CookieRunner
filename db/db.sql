drop table if exists cookies;
create table cookies (
  id integer primary key autoincrement,
  name varchar(255) not null,
  calories float not null
);
