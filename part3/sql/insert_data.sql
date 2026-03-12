-- Insert initial data into the database

-- Insert Administrator User
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$6D/A418HGqInNHr.syUNf.HAyxcK6Uz2FB4yuiOQwSpytaoD48TTG',
    1
)
ON CONFLICT(id) DO UPDATE SET
    first_name = excluded.first_name,
    last_name = excluded.last_name,
    email = excluded.email,
    password = excluded.password,
    is_admin = excluded.is_admin;

-- Insert Initial Amenities
INSERT INTO amenities (id, name)
VALUES 
    ('2767d121-c1b4-4d16-a816-0f5113ab06d0', 'WiFi'),
    ('bcf813cf-1fd0-4a7f-b69d-d4167331aaa1', 'Swimming Pool'),
    ('32561383-c728-4ba3-9fd2-cb7ceab79fca', 'Air Conditioning')
ON CONFLICT(id) DO UPDATE SET
    name = excluded.name;
