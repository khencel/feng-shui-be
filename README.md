All the codes is in master branch
This is the raw query for the report

SELECT
    DATE_TRUNC('month', r.pickup_time) AS month,
    CONCAT(u.first_name, ' ', u.last_name) AS driver,
    COUNT(*) AS trip_count
FROM rides_ride r
INNER JOIN users_user u
    ON r.id_driver = u.id_user
WHERE r.dropoff_time IS NOT NULL
  AND r.dropoff_time - r.pickup_time > INTERVAL '1 hour'
  AND u.role = 'driver'
GROUP BY
    DATE_TRUNC('month', r.pickup_time),
    u.id_user,
    u.first_name,
    u.last_name
ORDER BY
    month,
    u.id_user;


After migration please run custom command "seed_data" for populate database for initial data, then run also custom command "populate_pickup_locations" for populate pickup_location field.
I also used PostGIS and use docker