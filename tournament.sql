-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Creating database tournament
CREATE DATABASE tournament;

-- Connecting to the database
\c tournament

-- Creating table for players
CREATE TABLE players (id serial primary key, name text);

-- Creating table for match results information
CREATE TABLE matches (p1 integer references players(id), p2 integer references players(id), winner integer);

-- I don't know how to comment this view, but the idea is the following
-- First, make the table with id, name and amount of games played
-- Second, combine it with the table which counts on how many games 
-- were won by player
-- Third, do the sorting, by wins, and then by games played.

CREATE VIEW player_standings AS
SELECT temp.id, temp.name, count(matches.winner) as wins, temp.games as matches
FROM (
	SELECT id, name, COALESCE(m1,0)+COALESCE(m2,0) as games
	FROM players
	LEFT JOIN (
		SELECT matches.p1, count(matches.p1) as m1
		FROM matches GROUP BY matches.p1) 
	AS matches1
	ON (players.id = matches1.p1)
	LEFT JOIN (
		SELECT matches.p2, count(matches.p2) as m2
		FROM matches GROUP BY matches.p2) 
	AS matches2
	ON (players.id = matches2.p2)) as temp
LEFT JOIN matches
ON temp.id = matches.winner
GROUP BY temp.id, temp.name, temp.games
ORDER BY wins DESC, matches;