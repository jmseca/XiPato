DROP TABLE IF EXISTS sold;
DROP TABLE IF EXISTS possible_repeated_ad;
DROP TABLE IF EXISTS ad_with_return;
DROP TABLE IF EXISTS car_ad;
DROP TABLE IF EXISTS website;
DROP TABLE IF EXISTS car;

-- Tables --

create table car (
    car_id  decimal(9,0) GENERATED ALWAYS AS IDENTITY,
    brand   varchar(30),
    model   varchar(30),
    unique(brand, model)
    primary key (car_id)
);

create table website (
    site_name    varchar(20),
    primary key (site_name)
);

create table car_ad (
    ad_id           decimal(9,0)    GENERATED ALWAYS AS IDENTITY,
    car_id          decimal(9,0),
    price           decimal(7,2)    NOT NULL,
    year            decimal(4,0)    NOT NULL,
    ad_url          varchar(200),
    kms             decimal(9,0)    NOT NULL,
    site_name       varchar(20),
    scraped_date    timestamp,
    unique(car_id, price, year, kms, scraped_date)
    foreign key(car_id) references car(car_id),
    foreign key(site_name) references website(site_name),
    primary key(ad_id)
);

create table ad_with_return (
    ad_id               decimal(9,0),
    expected_return     decimal(7,0),
    foreign key(ad_id) references car_ad(ad_id) on delete cascade,
    primary key(ad_id)
);

create table possible_repeated_ad (
    ad_id           decimal(9,0),
    same_ad_url     varchar(200),
    foreign key(ad_id) references car_ad(ad_id)
    primary key(ad_id, same_ad_url)
);

create table sold (
    car_id      decimal(9,0),
    price       decimal(7,2),
    days_online decimal(4,0),
    year        decimal(4,0),
    kms         decimal(9,0),
    count       decimal(6,0),
    foreign key(car_id) references car(car_id),
    primary key(car_id, price, days_online, year, kms, count)
);