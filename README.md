# Tournament Results Project

## Description

The program keeps track of players and matches in a game tournament according to the Swiss system for pairing players. Players are not eliminated, and each player is paired with another player with the same number of wins, or as close as possible.

## Running the program
1. Required: [Python] (https://www.python.org/downloads/) (requires v2.7.x); [Bleach module for Python] (https://pypi.python.org/pypi/bleach); [Psycopg module for Python] (http://initd.org/psycopg/docs/install.html); [PostgreSQL] (http://www.postgresql.org/)
2. Clone the repo: git clone https://github.com/dmitiris/tournament.git
   or download all files in one directory
3. To build and access database run psql followed by \i tournament.sql in shell
4. Then run python console by typing in shell "python"
5. In python type "import tournament"

## Functions
a) Register players: tournament.registerPlayer(name), where name is the Player's name.
b) Do pairings: swissPairings()
c) Write results: reportMatch(winner, looser), where winner and looser are Player's ids.