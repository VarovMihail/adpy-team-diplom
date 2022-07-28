create table users
(
	user_id serial primary key, 
	id varchar(20) unique not null
);

create table like_list
(
	like_id serial primary key,
	user_name varchar(40) not null,
	link varchar(40) not null,
	id varchar(20) references users(id)
);

create table black_list
(
	black_id serial primary key,
	user_name varchar(40) not null,
	link varchar(40) not null,
	id varchar(20) references users(id)
);