-- DROP
DROP TRIGGER IF EXISTS ad_sold

CREATE OR REPLACE FUNCTION move_ad_to_sold () RETURNS TRIGGER AS
    $$ DECLARE similar_sold integer;
    BEGIN
        SELECT count(1) INTO similar_sold
        FROM sold
        WHERE OLD.brand=brand AND OLD.model=model AND OLD.price=price
        AND OLD.year=year AND OLD.days_online=days_online
        AND OLD.site_name=site_name AND OLD.kms=kms;

        IF (similar_sold > 0) 
        THEN
            UPDATE sold
            SET count = count + 1
            WHERE OLD.brand=brand AND OLD.model=model AND OLD.price=price
            AND OLD.year=year AND OLD.days_online=days_online
            AND OLD.site_name=site_name AND OLD.kms=kms;
            -- change this (days_online does not exist in ads)
        ELSE
            INSERT INTO sold values (OLD.);
            -- change this (need to calculate days online from timestamp)
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

CREATE TRIGGER ad_sold BEFORE DELETE ON car_ad
FOR EACH ROW EXECUTE PROCEDURE move_ad_to_sold();