CREATE TABLE Themes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    theme VARCHAR(64)
);

CREATE TABLE Topics(
    id INT AUTO_INCREMENT PRIMARY KEY,
    theme_id INT,
    topic_text VARCHAR(64),
    FOREIGN KEY (theme_id) REFERENCES Themes(id)
);

CREATE TABLE Topic_pairs(
    id INT AUTO_INCREMENT PRIMARY KEY,
    theme_id INT,
    topic1_id INT,
    topic2_id INT,
    FOREIGN KEY (theme_id) REFERENCES Themes(id),
    FOREIGN KEY (topic1_id) REFERENCES Topics(id),
    FOREIGN KEY (topic2_id) REFERENCES Topics(id)
);

CREATE TABLE Players(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64),
    assigned_topic_id INT,
    keyword VARCHAR(64),
    FOREIGN KEY (assigned_topic_id) REFERENCES Topics(id)
);