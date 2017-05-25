drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  username text not null,
  email text not null,
  pw_hash text not null
);

drop table if exists message;
create table message (
  message_id integer primary key autoincrement,
  author_id integer not null,
  text text not null,
  pub_date integer
);

drop table if exists proxy;
create table proxy(
  ip text not null,
  port integer not null,
  provider text not null,
  add_date integer not null,
  check_date integer,
  anonymity_level integer,
  PRIMARY KEY (ip, port)
);
