CREATE TABLE IF NOT EXISTS admin (
  user_id BIGINT PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS winner (
  user_id BIGINT PRIMARY KEY,
  battle_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  FOREIGN KEY(battle_id) REFERENCES battle(battle_id)
);

CREATE TABLE IF NOT EXISTS battle (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  battle_id INTEGER,
  beatmaker_host_id BIGINT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  is_open INTEGER NOT NULL,
  FOREIGN KEY(beatmaker_host_id) REFERENCES beatmaker(user_id),
  CHECK (is_open IN (0, 1))
);

CREATE TABLE IF NOT EXISTS beatmaker (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  battle_id INTEGER NOT NULL,
  user_id BIGINT NOT NULL,
  user_name VARCHAR(60) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  FOREIGN KEY(battle_id) REFERENCES battle(battle_id),
  UNIQUE(battle_id, user_id)
);

CREATE TABLE IF NOT EXISTS voting (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id BIGINT NOT NULL,
  battle_id INTEGER NOT NULL,
  FOREIGN KEY(battle_id) REFERENCES battle(battle_id)
);

CREATE TABLE IF NOT EXISTS vote (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  battle_id INTEGER NOT NULL,
  user_id BIGINT NOT NULL,
  first_beatmaker BIGINT NOT NULL,
  second_beatmaker BIGINT NOT NULL,
  third_beatmaker BIGINT NOT NULL,
  FOREIGN KEY(battle_id) REFERENCES battle(battle_id),
  FOREIGN KEY(user_id) REFERENCES beatmaker(user_id),
  FOREIGN KEY(first_beatmaker) REFERENCES bitmaker(user_id),
  FOREIGN KEY(second_beatmaker) REFERENCES bitmaker(user_id),
  FOREIGN KEY(third_beatmaker) REFERENCES bitmaker(user_id),
  UNIQUE(battle_id, user_id)
);

