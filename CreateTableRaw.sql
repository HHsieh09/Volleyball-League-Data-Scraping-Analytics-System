CREATE TABLE IF NOT EXISTS Matches (
    match_cup_id VARCHAR(255) PRIMARY KEY,
    match_id VARCHAR(255),
    tournament_id INT,
    match_date DATE,
    match_time TIME,
    arena VARCHAR(255),
    duration TIME,
    match_type VARCHAR(255)
);

-- 建 Match_Score 表
CREATE TABLE IF NOT EXISTS Match_Score (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    match_cup_id VARCHAR(255),
    match_team VARCHAR(255),
    set1 INT,
    set2 INT,
    set3 INT,
    set4 INT,
    set5 INT,
    FOREIGN KEY (match_cup_id) REFERENCES Matches(match_cup_id)
);

-- 建 Match_Referee 表
CREATE TABLE IF NOT EXISTS Match_Referee (
    match_referee_id INT AUTO_INCREMENT PRIMARY KEY,
    match_cup_id VARCHAR(255),
    first_referee VARCHAR(255),
    second_referee VARCHAR(255),
    FOREIGN KEY (match_cup_id) REFERENCES Matches(match_cup_id)
);

-- 建 Match_Coach 表
CREATE TABLE IF NOT EXISTS Match_Coach (
    match_coach_id INT AUTO_INCREMENT PRIMARY KEY,
    match_cup_id VARCHAR(255),
    team VARCHAR(255),
    head_coach VARCHAR(255),
    assistant_coach1 VARCHAR(255),
    assistant_coach2 VARCHAR(255),
    FOREIGN KEY (match_cup_id) REFERENCES Matches(match_cup_id)
);

-- 建 Player_Stats 表
CREATE TABLE IF NOT EXISTS Player_Stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    match_cup_id VARCHAR(255),
    team VARCHAR(255),
    number INT,
    name VARCHAR(255),
    position VARCHAR(50),
    attack_point INT,
    attack_total INT,
    block_point INT,
    serve_point INT,
    serve_total INT,
    receive_nice INT,
    receive_total INT,
    dig_nice INT,
    dig_total INT,
    set_nice INT,
    set_total INT,
    total_points INT,
    FOREIGN KEY (match_cup_id) REFERENCES Matches(match_cup_id)
);
