"""
Quick check - How many games are actually in the database?
"""

import sqlite3
import os

# Find database
possible_dbs = [
    'data/odds_data.db',
    'data/player_props.db',
    'data/enhanced_odds.db'
]

DB_PATH = None
for db in possible_dbs:
    if os.path.exists(db):
        DB_PATH = db
        break

if not DB_PATH:
    print("ERROR: No database found!")
    exit(1)

print(f"Checking: {DB_PATH}\n")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Count total unique games
cursor.execute("""
    SELECT COUNT(DISTINCT event_id) as count FROM player_props
""")
total_games = cursor.fetchone()[0]
print(f"Total unique games in database: {total_games}")

# List all games with dates
cursor.execute("""
    SELECT DISTINCT
        event_id,
        sport_key,
        home_team,
        away_team,
        commence_time,
        DATE(commence_time) as game_date,
        COUNT(*) as prop_count
    FROM player_props
    GROUP BY event_id
    ORDER BY commence_time
""")

games = cursor.fetchall()
print(f"\nAll {len(games)} games in database:\n")

for i, game in enumerate(games, 1):
    print(f"{i:2d}. {game['away_team']} @ {game['home_team']}")
    print(f"    Date: {game['game_date']}, Time: {game['commence_time']}")
    print(f"    Props: {game['prop_count']}")

# Check tomorrow specifically
cursor.execute("SELECT date('now', '+1 day') as tomorrow")
tomorrow = cursor.fetchone()['tomorrow']
print(f"\n\nSQLite thinks tomorrow is: {tomorrow}")

cursor.execute("""
    SELECT COUNT(DISTINCT event_id) as count
    FROM player_props
    WHERE date(commence_time) = date('now', '+1 day')
""")
tomorrow_count = cursor.fetchone()[0]
print(f"Games tomorrow (SQLite filter): {tomorrow_count}")

conn.close()