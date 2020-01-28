create schema currency;

create table currency.currency_type(
    id serial primary key,
    name text not null,
    rate_in_rub money not null
);

insert into currency.currency_type(name, rate_in_rub) values
    ('RUB', 1),
    ('EUR', 1),
    ('USD', 1),
    ('GPB', 1),
    ('BTC', 1);

create table currency.customer(
    id serial primary key,
    email text not null,
    password text not null,

    balance money not null default 0,
    currency_type_id integer not null default 1,

    cretead timestamp not null default now()
);

create table currency.transaction(
    id serial primary key,
    from_customer_id integer not null references currency.customer(id),
    to_customer_id integer not null references currency.customer(id),
    transaction_value money not null,
    currency_type_id integer not null default 1,
    cretead timestamp not null default now()
)
