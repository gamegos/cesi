drop table if exists userinfo;
create table userinfo(username varchar(30) PRIMARY KEY NOT NULL, password varchar(50) NOT NULL, type INT NOT NULL);
insert into userinfo values('admin', '$argon2i$v=19$m=512,t=2,p=2$+Z9TqhVizBlDCMF4D0FIqQ$HXWeRS32Oo0h2+HEhGFMkw', 0);
