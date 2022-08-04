-- DROP
DROP TRIGGER IF EXISTS ad_sold ON car_ad;
DROP TRIGGER IF EXISTS repeated_ad ON car_ad;

CREATE OR REPLACE FUNCTION move_ad_to_sold () RETURNS TRIGGER AS
    $$ 
    DECLARE similar_sold integer;
    DECLARE ad_days_online decimal(5,0);

    BEGIN
        SELECT count(1) INTO similar_sold
        FROM sold
        WHERE OLD.car_id=car_id AND OLD.price=price
        AND OLD.year=year AND OLD.kms=kms;

        IF (similar_sold > 0) 
        THEN
            UPDATE sold
            SET count = count + 1
            WHERE OLD.brand=brand AND OLD.model=model AND OLD.price=price
            AND OLD.year=year AND OLD.kms=kms;
        ELSE
            SELECT EXTRACT(DAT FROM (NOW() - OLD.days_online)) INTO ad_days_online;
            INSERT INTO sold values (OLD.car_id, OLD.price, ad_days_online, OLD.year, OLD.kms, 1);
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

CREATE TRIGGER ad_sold BEFORE DELETE ON car_ad
FOR EACH ROW EXECUTE PROCEDURE move_ad_to_sold();


CREATE OR REPLACE FUNCTION check_for_repeated_ad () RETURNS TRIGGER AS
    $$ 
    DECLARE sim_ad decimal(9,0);
    DECLARE cursor_car_ad CURSOR FOR
        SELECT ad_id
        FROM car_ad
        WHERE NEW.car_id=car_id AND NEW.price=price
        AND NEW.year=year AND NEW.kms=kms;
    DECLARE control_var decimal(5,0);
    BEGIN
        control_var = 0;
        OPEN cursor_car_ad;
        LOOP
            FETCH cursor_car_ad INTO sim_ad;
            EXIT WHEN NOT FOUND;
            INSERT INTO possible_repeated_ad VALUES (sim_ad, NEW.ad_url);
            control_var = 1;
        END LOOP;
        IF (control_var = 0)
        THEN
            RETURN NEW;
        ELSE
            RETURN NULL;
        END IF;
    END;
    $$ LANGUAGE plpgsql;

CREATE TRIGGER repeated_ad BEFORE INSERT ON car_ad
FOR EACH ROW EXECUTE PROCEDURE check_for_repeated_ad();