-- Build Tables in Order of Need

-- Score Table
    -- Used to hold modifiers for Ancestries
    -- May be used to hold Score values for Characters?
DROP TABLE IF EXISTS Scores;

CREATE TABLE Scores(
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    strength INT DEFAULT 0,
    dexterity INT DEFAULT 0,
    constitution INT DEFAULT 0,
    intelligence INT DEFAULT 0,
    wisdom INT DEFAULT 0,
    charisma INT DEFAULT 0,
    free INT DEFAULT 0);

DROP TABLE IF EXISTS Ancestries;

CREATE TABLE Ancestries(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    A_name VARCHAR(255) UNIQUE NOT NULL,
    A_size VARCHAR(255) NOT NULL,
    traits  VARCHAR(255) NOT NULL,
    health INT NOT NULL,
    speed VARCHAR(255) NOT NULL,
    scoreID INT NOT NULL,
    FOREIGN KEY (scoreID) REFERENCES Scores(id),
    A_description TEXT,
    languages VARCHAR(255) NOT NULL,
    abilities TEXT,
    source VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS Feats;

CREATE TABLE Feats(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL;
    F_name VARCHAR(255) UNIQUE NOT NULL,
    F_description TEXT NOT NULL,
    traits TEXT NOT NULL,
    source VARCHAR(255) NOT NULL,
    F_level INT NOT NULL
);