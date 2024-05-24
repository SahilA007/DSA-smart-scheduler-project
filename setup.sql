-- Create tables
CREATE TABLE venues (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE time_slots (
    id INTEGER PRIMARY KEY,
    slot TEXT NOT NULL
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Insert sample data
INSERT INTO venues (name) VALUES ('Room 101'), ('Room 102'), ('Room 103');
INSERT INTO time_slots (slot) VALUES ('Mon 9-11'), ('Mon 11-1'), ('Tue 9-11'), ('Tue 11-1'), ('Wed 9-11'), ('Wed 11-1');
INSERT INTO classes (name) VALUES ('Math 101'), ('Physics 201'), ('Chemistry 301');
