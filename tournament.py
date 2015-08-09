#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("TRUNCATE matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("TRUNCATE players CASCADE;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM players;")
    num = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Preparing QUERY and DATA
    SQL = "INSERT INTO players (name) VALUES (%s);"
    name = bleach.clean(name)
    data = (name, )
    # Working with PostgreSQL
    conn = connect()
    cur = conn.cursor()
    cur.execute(SQL, data)
    conn.commit()
    cur.close()
    conn.close()
    # Line is not required, but somehow I feel it would be nice to know
    # the result
    print "Player %s has been registered" % name 


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    # player_standings is a view in PostgreSQL  
    cur.execute("SELECT * FROM player_standings;")
    player_list = cur.fetchall()
    cur.close()
    conn.close()
    return player_list


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Preparing QUERY and DATA
    winner = int(winner)
    loser = int(loser)
    # Wondering if we always enter winner first, do we really need
    # winner column in matches table?
    SQL = "INSERT INTO matches (p1, p2, winner) VALUES (%s, %s, %s);"
    data = (winner, loser, winner,)
    # Working with PostgreSQL
    conn = connect()
    cur = conn.cursor()
    cur.execute(SQL, data)
    cur.close()
    conn.commit()
    conn.close()
    
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Get players' standings
    ps = playerStandings()
    return [(ps[i][0], # first player id
             ps[i][1], # first player name
             ps[i+1][0], # second player id
             ps[i+1][1] # second player name
             ) for i in range(0, len(ps),2)]

