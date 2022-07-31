-- DROP
DROP TRIGGER IF EXISTS ad_sold

CREATE OR REPLACE FUNCTION move_ad_to_sold () RETURNS TRIGGER AS
    $$
    BEGIN
    similar_sold := 0
    SELECT count(1) INTO similar_sold
    FROM sold
    WHERE OLD.brand=brand AND OLD.model=model AND OLD.price=price
    AND

    END;
    $$ LANGUAGE plpgsql;

CREATE TRIGGER ad_sold BEFORE DELETE ON car_ad
FOR EACH ROW EXECUTE PROCEDURE move_ad_to_sold();