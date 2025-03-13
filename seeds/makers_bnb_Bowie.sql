DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP TABLE IF EXISTS spaces CASCADE;
DROP SEQUENCE IF EXISTS spaces_id_seq;
DROP TABLE IF EXISTS bookings CASCADE;
DROP SEQUENCE IF EXISTS bookings_id_seq;

CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    encrypted_password TEXT
);

CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name TEXT,
    location TEXT,
    description TEXT,
    price_per_night INT,
    dates_available_dict JSON, 
    image_content TEXT,
    user_id int,
        constraint fk_user foreign key(user_id)
        references users(id)
        on delete cascade
);

CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    requested_dates TEXT,
    user_id int,
        constraint fk_user foreign key(user_id)
        references users(id)
        on delete cascade,
    space_id int,
        constraint fk_space foreign key(space_id)
        references spaces(id)
        on delete cascade,
    approved BOOLEAN
);

INSERT INTO users (username, encrypted_password) VALUES ('Luis', 'f5d44b29add0d1a87b9edc82e7c5a9fd'); -- Password: IloveTaylorSwift
INSERT INTO users (username, encrypted_password) VALUES ('Joseph', '6380dcbb2728aa384ed16fc1cf98b1f0'); -- Password: Idoto
INSERT INTO users (username, encrypted_password) VALUES ('jackmisner', '5e075470c9298a362f78901a75c0d288');

INSERT INTO spaces (name, location, description, price_per_night, dates_available_dict, image_content, user_id) VALUES ('Makers Villa', 'London', 'Beautiful refurbished industrial warehouse', 150, '{"2025-03-12": true, "2025-03-13": true, "2025-03-14": false}', 'https://as-images.imgix.net/e0e91fbfcbda875d65ccfc75fcc8d60a-DRC_9449.jpg', 1);
INSERT INTO spaces (name, location, description, price_per_night, dates_available_dict, image_content, user_id) VALUES ('Josephs farm', 'Gorenflos', 'Traditional French potato farm. Perfect for couple retreat', 90, '{"2025-07-5" : false}', 'https://i.redd.it/1z3atrfp76d01.jpg', 2);
INSERT INTO spaces (name, location, description, price_per_night, dates_available_dict, image_content, user_id) VALUES ('Makers Retreat', 'Bali', 'Perfect for a digital detox after a very long bootcamp.', 160, '{"2025-02-01":true}', 'https://static1.squarespace.com/static/5b43674975f9ee7f0ff1df28/t/62fe3fd35115865134a6985f/1660829657669/bali-yoga-retreat-center-ubud-shala.jpg?format=1500w', 1);
INSERT INTO spaces (name, location, description, price_per_night, dates_available_dict, image_content, user_id) VALUES ('Bowser Castle', 'Hell', 'Welcome to Bowser Castle. Make you sure you bring some sunscreen.', 1, '{"2024-12-21":true}', 'https://mario.wiki.gallery/images/thumb/b/b0/BowsersCastleMKW.png/1600px-BowsersCastleMKW.png', 1);
INSERT INTO spaces (name, location, description, price_per_night, dates_available_dict, image_content, user_id) VALUES ('Rivendell', 'Far away', 'Perfect for a city break. Quiet and relaxing, you will share the castle with the lovely habitants.', 200,'{"2023-06-14":true}', 'https://collectiveshara426.weebly.com/uploads/1/2/3/7/123705642/794705490.jpg', 2)

