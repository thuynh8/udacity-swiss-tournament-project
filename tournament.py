#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM match;")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM player;")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM player;")
    number_of_players = c.fetchone()[0]
    DB.close()
    return number_of_players

def registerPlayer(name):
    """Adds a player to the tournament database."""
    player_name = str(name)
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO player (name) VALUES (%s);", (player_name,))
    DB.commit()
    DB.close()

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
    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT player.id, player.name, SUM(match.score) AS wins, COUNT(match.match_id) AS matches
                 FROM player LEFT JOIN match 
                 ON player.id = match.player_id 
                 GROUP BY player.id ORDER BY wins DESC;""")
    players_info = []
    for player in c.fetchall():
        if player[2] == None:
            players_info.append((player[0],player[1],0,int(player[3])))
        else:
            players_info.append((player[0],player[1],player[2],int(player[3])))
    DB.close()
    return players_info


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()

    # Assign match_id to a sigle match between two players
    c.execute("SELECT MAX(match_id) FROM match;")
    most_recent_match_id = c.fetchone()[0]
    if most_recent_match_id == None:
        most_recent_match_id = 0
        match_id = most_recent_match_id + 1
    else:
        match_id = most_recent_match_id + 1

    # Insert match_id, winner, and loser info into match table
    c.execute("INSERT INTO match VALUES(%s, %s, 1)", (match_id,int(winner),))
    c.execute("INSERT INTO match VALUES(%s, %s, 0)", (match_id,int(loser),))
    DB.commit()
    DB.close()
 
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
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(wins) FROM standing;")
    num_wins = c.fetchone()[0]
    if num_wins == 0:
        c.execute("""SELECT a.id, a.name, b.id, b.name
                     FROM standing as a,
                          standing as b
                     WHERE a.matches = b.matches
                     AND a.id < b.id
                     LIMIT 4;""")
    if num_wins != 0:
        c.execute("""SELECT a.id, a.name, b.id, b.name
                     FROM standing as a,
                          standing as b
                     WHERE a.wins = b.wins
                     AND a.matches = b.matches
                     AND a.id < b.id
                     LIMIT 4;""")
    pairs = []
    for pair in c.fetchall():
        pairs.append(pair)
    DB.close()
    return pairs

