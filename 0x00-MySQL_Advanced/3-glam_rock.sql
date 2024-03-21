--SQL script that lists all bands with Glam rock as their main style,
--ranked by their longevity
SELECT band_name, 
       (YEAR('2022-01-01') - CAST(SUBSTRING_INDEX(formed, '-', 1) AS UNSIGNED)) as lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
