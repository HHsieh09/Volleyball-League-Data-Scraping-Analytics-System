CREATE TABLE IF NOT EXISTS Tournament (
    tournament_id INT PRIMARY KEY,
    tournament_name VARCHAR(255),
    year INT
);

CREATE TABLE IF NOT EXISTS Team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Tournament_Team (
    tournament_team_id INT AUTO_INCREMENT PRIMARY KEY,
    tournament_id INT,
    team_id INT,
    FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

CREATE TABLE IF NOT EXISTS Matches (
    match_cup_id VARCHAR(255) PRIMARY KEY,
    match_id INT,
    tournament_id INT,
    match_date DATE,
    match_time TIME,
    arena VARCHAR(255),
    duration TIME,
    match_type VARCHAR(255),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id)
);

CREATE TABLE IF NOT EXISTS Match_Team (
    match_team_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    team_id INT,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (team_id) REFERENCES Tournament_Team(team_id)
);

CREATE TABLE IF NOT EXISTS Match_Score (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    match_team_id INT,
    set1 INT,
    set2 INT,
    set3 INT,
    set4 INT,
    set5 INT,
    FOREIGN KEY (match_team_id) REFERENCES Match_Team(match_team_id)
);

CREATE TABLE IF NOT EXISTS Referee (
    referee_id INT AUTO_INCREMENT PRIMARY KEY,
    referee_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Match_Referee (
    match_referee_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    referee_id INT,
    referee_type VARCHAR(50),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (referee_id) REFERENCES Referee(referee_id)
);

CREATE TABLE IF NOT EXISTS Coach (
    coach_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    coach_name VARCHAR(255),
    coach_role ENUM('Head Coach', 'Assistant Coach 1', 'Assistant Coach 2'),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

CREATE TABLE IF NOT EXISTS Player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(255),
    player_number INT,
    position VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Tournament_Player (
    tournament_player_id INT AUTO_INCREMENT PRIMARY KEY,
    tournament_team_id INT,
    player_id INT,
    FOREIGN KEY (tournament_team_id) REFERENCES Tournament_Team(tournament_team_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

CREATE TABLE IF NOT EXISTS Player_Stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    match_team_id INT,
    tournament_player_id INT,
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
    FOREIGN KEY (match_team_id) REFERENCES Match_Team(match_team_id),
    FOREIGN KEY (tournament_player_id) REFERENCES Tournament_Player(tournament_player_id)
);