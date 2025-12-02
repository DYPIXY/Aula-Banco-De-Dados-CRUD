drop table user, passwords, note_type, notes;

create table user(
	id int not null primary key auto_increment,
	nome varchar(255) not null,
	email varchar(320)
);

create table passwords(
	user_id int not null unique
	,password varchar(256) not null
	,salt varchar(32)
	,foreign key(user_id) references user(id)
);

create table note_type
(
	id int not null primary key
	,tipo varchar(64) not null
	,definitons json
);

create table notes(
	id int not null primary key auto_increment,
	texto text,
	user_id int not null,
	tipo_id int,
	foreign key(user_id) references user(id),
	foreign key(tipo_id) references note_type(id)
);

## insert pra popular um mockup

insert into note_type(id, tipo, definitons)
values
(1, 'Urgente', '{"color":"yellow", "text":"bold"}'),
(2, 'Normal', null),
(3, 'Temporária', '{"expires":"2025-12-25"}');

insert into user(id, nome, email)
values(1, 'usuario_teste', 'usuario.teste@teste.com');

#senha = teste
#salt =
insert into passwords(user_id, password, salt)
values(1, '1c29b697e5a2ca8f1d092097a4a3f0017d3d54e21064e69d191f07aa1807b174', '12345678');
