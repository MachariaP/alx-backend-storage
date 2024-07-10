-- This SQL script lists all bands with Glam rock as their style
-- ranked by their longevity

SELECT band_name, IF(split = '0' OR split IS NULL, 2022 - formed, split - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style) > 0 OR style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
