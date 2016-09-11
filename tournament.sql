-- Table definitions for the tournament project.

-- Create and connect to tournament database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Player Table:
CREATE TABLE player (id SERIAL PRIMARY KEY, 
					 name TEXT);

-- Match Table:
CREATE TABLE match (match_id INTEGER, 
					player_id INTEGER REFERENCES player(id),
					score INTEGER DEFAULT 0,
					PRIMARY KEY(match_id,player_id));

-- Standing View:
CREATE VIEW standing as SELECT player.id, player.name, SUM(match.score) AS wins, COUNT(match.match_id) AS matches
                 FROM player LEFT JOIN match 
                 ON player.id = match.player_id 
                 GROUP BY player.id ORDER BY wins DESC;
