-- Build Tables in Order of Need

-- Score Table
    -- Used to hold modifiers for Ancestries
    -- May be used to hold Score values for Characters?
DROP TABLE IF EXISTS Scores;

CREATE TABLE Scores(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    strength INT DEFAULT 0;
    dexterity INT DEFAULT 0;
    constitution INT DEFAULT 0;
    intelligence INT DEFAULT 0;
    wisdom INT DEFAULT 0;
    charisma INT DEFAULT 0;
    free INT DEFAULT 0;
)

DROP TABLE IF EXISTS Ancetries;

CREATE TABLE Ancetries(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    A_name VARCHAR(255) UNIQUE NOT NULL,
    A_size ENUM('Small', 'Medium', 'Large') NOT NULL,
    traits  VARCHAR(255) NOT NULL,
    health INT NOT NULL,
    speed INT NOT NULL
    scoreID INT NOT NULL,
        FOREIGN KEY (scoreID) REFERENCES Scores(id),
    A_description TEXT,
    languages VARCHAR(255) NOT NULL
    senses VARCHAR(255),
    source VARCHAR(255)
)