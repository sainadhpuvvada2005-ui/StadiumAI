INSERT INTO roles(name, description) VALUES ('fan','Tournament visitor'),('volunteer','Venue volunteer'),('organizer','Operations organizer'),('admin','System administrator') ON CONFLICT DO NOTHING;
INSERT INTO gates(code,name,latitude,longitude,accessibility,current_wait_minutes,congestion_score) VALUES
('A','North Gate',25.960,-80.239,true,8,.34),('B','Metro Gate',25.961,-80.236,true,28,.88),('C','West Gate',25.956,-80.243,false,16,.62),('D','East Gate',25.955,-80.241,true,6,.28) ON CONFLICT DO NOTHING;
INSERT INTO matches(home_team,away_team,venue,starts_at,status) VALUES ('USA','Canada','Miami Stadium','2026-06-15 19:00:00','scheduled'),('Brazil','France','Miami Stadium','2026-06-20 21:00:00','scheduled');
INSERT INTO parking(name,total_spaces,free_spaces,accessible_spaces,latitude,longitude) VALUES ('Lot A',1200,240,22,25.953,-80.246),('Lot C',1800,728,46,25.965,-80.235),('Accessible South',220,64,64,25.952,-80.238);
INSERT INTO crowd(zone,density,queue_length,wait_minutes,ingress_rate) VALUES ('Gate B',.88,620,28,900),('Gate D',.28,90,6,420),('Food Court North',.54,120,9,260),('Exit D',.31,80,5,180);
INSERT INTO transport(mode,route_name,eta_minutes,crowd_level,carbon_grams,accessibility) VALUES ('metro','Line 2 Stadium Express',4,.72,40,true),('bus','Route 26 Shuttle',11,.45,180,true),('taxi','North rideshare loop',18,.64,2100,false),('walking','Riverwalk route',24,.25,0,true);
INSERT INTO food_courts(name,zone,queue_minutes,open_stalls,vegetarian,halal) VALUES ('North Market','North Stand',7,14,true,true),('South Grill','South Stand',18,8,true,true),('East Snacks','East Concourse',5,6,true,false);
INSERT INTO energy(zone,kwh) VALUES ('North Stand',9200),('South Stand',7600),('Pitch Lighting',5000);
INSERT INTO water(zone,liters) VALUES ('Restrooms North',32000),('Food Service',28400),('Pitch',22000);
INSERT INTO waste(zone,kilograms,recycled_percent) VALUES ('North Stand',1800,62),('South Stand',2300,48),('Food Service',1500,55);
