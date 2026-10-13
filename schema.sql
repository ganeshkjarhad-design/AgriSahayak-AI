PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    location TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    location TEXT NOT NULL,
    skill TEXT NOT NULL,
    experience_years INTEGER DEFAULT 0,
    equipment TEXT,
    daily_rate REAL DEFAULT 0,
    rating REAL DEFAULT 0,
    available_days TEXT DEFAULT 'Mon,Tue,Wed,Thu,Fri,Sat',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER NOT NULL,
    worker_id INTEGER NOT NULL,
    work_type TEXT NOT NULL,
    booking_date TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id),
    FOREIGN KEY (worker_id) REFERENCES workers(id)
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    image_name TEXT,
    prediction TEXT NOT NULL,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id)
);

CREATE TABLE IF NOT EXISTS disease_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT UNIQUE NOT NULL,
    crop TEXT NOT NULL,
    disease TEXT NOT NULL,
    prevention TEXT,
    treatment_note TEXT
);

INSERT OR IGNORE INTO farmers(name,phone,location) VALUES
('Demo Farmer','9999999999','Pune');

INSERT OR IGNORE INTO workers(name,phone,location,skill,experience_years,equipment,daily_rate,rating,available_days) VALUES
('Ramesh Patil','9000000001','Pune','Crop Spraying',5,'Power Sprayer',900,4.6,'Mon,Tue,Wed,Thu,Fri,Sat'),
('Suresh Jadhav','9000000002','Pimpri','Harvesting',7,'Harvest Tools',800,4.4,'Tue,Wed,Thu,Sat'),
('Amit Shinde','9000000003','Lonavala','Crop Spraying',3,'Battery Sprayer',700,4.2,'Mon,Wed,Fri,Sat'),
('Vikas More','9000000004','Pune','Planting',4,'Planting Tools',650,4.5,'Mon,Tue,Thu,Fri');

INSERT OR IGNORE INTO disease_info(class_name,crop,disease,prevention,treatment_note) VALUES
('Tomato___healthy','Tomato','Healthy','Maintain balanced irrigation and field sanitation.','No disease treatment is indicated by the model.'),
('Tomato___Early_blight','Tomato','Early Blight','Remove affected leaves and avoid prolonged leaf wetness.','Consult local agricultural guidance and follow the approved product label if treatment is needed.'),
('Tomato___Late_blight','Tomato','Late Blight','Use clean planting material and avoid overhead irrigation when possible.','Seek local agricultural advice promptly and follow the approved product label.'),
('Potato___healthy','Potato','Healthy','Maintain field sanitation and balanced irrigation.','No disease treatment is indicated by the model.'),
('Potato___Early_blight','Potato','Early Blight','Remove infected plant material and maintain good crop hygiene.','Consult local agricultural guidance and follow the approved product label.'),
('Potato___Late_blight','Potato','Late Blight','Use healthy seed and monitor crops regularly.','Seek local agricultural advice promptly and follow the approved product label.'),
('Pepper,_bell___healthy','Bell Pepper','Healthy','Use clean seedlings and maintain field hygiene.','No disease treatment is indicated by the model.'),
('Pepper,_bell___Bacterial_spot','Bell Pepper','Bacterial Spot','Use clean planting material and reduce leaf wetness.','Consult local agricultural guidance and follow the approved product label.')
