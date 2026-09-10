CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE public.geodaten (
    id SERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    geom GEOMETRY(Geometry, 4326),
    zentrum GEOMETRY(Point, 4326),
    created_at TIMESTAMP DEFAULT NOW()
);
-- Spatialer Index für performantere Abfragen
CREATE INDEX IF NOT EXISTS idx_geodaten_geom ON public.geodaten USING GIST (geom);
