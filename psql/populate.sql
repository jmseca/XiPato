

-- Tables --

create table car (
    brand   varchar(30),
    model   varchar(30),
    primary key (brand, model)
);

create table website (
    site_name    varchar(20),
    primary key (site_name)
);

create table car_ad (
    brand           varchar(30),
    model           varchar(30),
    price           decimal(7,2)    NOT NULL,
    year            decimal(4,0)    NOT NULL,
    ad_url          varchar(150),
    kms             decimal(9,0)    NOT NULL,
    site_name       varchar(20),
    scraped_date    timestamp,
    foreign key(brand,model) references car(brand,model),
    foreign key(site_name) references website(site_name),
    primary key(ad_url)
);

create table sold (
    brand       varchar(30),
    model       varchar(30),
    price       decimal(7,2),
    days_online decimal(4,0),
    site_name   varchar(20),
    year        decimal(4,0),
    kms         decimal(9,0),
    count       decimal(6,0),
    foreign key(brand,model) references car(brand,model),
    foreign key(site_name) references website(site_name),
    primary key(brand, model, price, days_online, site_name, year, kms, count)
);