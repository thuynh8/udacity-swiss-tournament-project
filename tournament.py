#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()

    query = "DELETE FROM match;"
    cursor.execute(query)
    
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()

    query = "DELETE FROM player;"
    cursor.execute(query)

    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()

    query = "SELECT count(*) FROM player;"
    cursor.execute(query)
    number_of_players = cursor.fetchone()[0]

    db.close()
    return number_of_players

def registerPlayer(name):
    """Adds a player to the tournament database."""
    db, cursor = connect()

    parameter = (name,)   
    query = "INSERT INTO player (name) VALUES (%s);"
    cursor.execute(query, parameter)

    db.commit()
    db.close()

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
    db, cursor = connect()

    query = "SELECT * FROM standing;"
    cursor.execute(query)

    players_info = []
    for player in cursor.fetchall():
        if player[2] == None:
            players_info.append((player[0],player[1],0,int(player[3])))
        else:
            players_info.append((player[0],player[1],player[2],int(player[3])))

    db.close()
    return players_info


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()

    # Assign match_id to a sigle match between two players
    query = "SELECT MAX(match_id) FROM match;"
    cursor.execute(query)

    most_recent_match_id = cursor.fetchone()[0]
    if most_recent_match_id == None:
        most_recent_match_id = 0
        match_id = most_recent_match_id + 1
    else:
        match_id = most_recent_match_id + 1

    # Insert match_id, winner, and loser info into match table
    cursor.execute("INSERT INTO match VALUES(%s, %s, 1)", (match_id,int(winner),))
    cursor.execute("INSERT INTO match VALUES(%s, %s, 0)", (match_id,int(loser),))
    db.commit()
    db.close()
 
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
    db, cursor = connect()

    # Determine how many pairs needed based on number of players
    query1 = "SELECT COUNT(*) FROM player"
    cursor.execute(query1)
    num_players = cursor.fetchone()[0]
    number_of_pairs = num_players / 2

    # Pair players against each other
    query2 = "SELECT COUNT(wins) FROM standing;"
    cursor.execute(query2)

    num_wins = cursor.fetchone()[0]
    if num_wins == 0:
        cursor.execute("""SELECT a.id, a.name, b.id, b.name
                     FROM standing as a,
                          standing as b
                     WHERE a.matches = b.matches
                     AND a.id < b.id
                     LIMIT (%s);""", (number_of_pairs,))
    if num_wins != 0:
        cursor.execute("""SELECT a.id, a.name, b.id, b.name
                     FROM standing as a,
                          standing as b
                     WHERE a.wins = b.wins
                     AND a.matches = b.matches
                     AND a.id < b.id
                     LIMIT (%s);""", (number_of_pairs,))
    pairs = []
    for pair in cursor.fetchall():
        pairs.append(pair)

    db.close()
    return pairs

