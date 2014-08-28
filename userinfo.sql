drop table if exists userinfo;
create table userinfo(username varchar(30) PRIMARY KEY NOT NULL, password varchar(50) NOT NULL, type INT NOT NULL);
insert into userinfo values('admin', 'admin', 0);
