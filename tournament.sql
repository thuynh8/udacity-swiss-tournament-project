-- Table definitions for the tournament project.

# Drop table if table already exists
DROP TABLE IF EXISTS standing;
DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS player;

-- Player Table:
CREATE TABLE player (id SERIAL PRIMARY KEY, 
					 name TEXT);

-- Match Table:
CREATE TABLE match (match_id INTEGER, 
					player_id INTEGER REFERENCES player(id),
					score INTEGER DEFAULT 0,
					PRIMARY KEY(match_id,player_id));

-- Standing View Table:
CREATE VIEW standing as SELECT player.id, player.name, SUM(match.score) AS wins, COUNT(match.match_id) AS matches
                 FROM player LEFT JOIN match 
                 ON player.id = match.player_id 
                 GROUP BY player.id ORDER BY wins DESC;