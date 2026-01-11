import sqlite3
from datetime import datetime

conn = sqlite3.connect('data/odds_data.db')
cursor = conn.cursor()

# Check what dates we have
cursor.execute("""
    SELECT DISTINCT DATE(commence_time) as game_date, 
           COUNT(DISTINCT event_id) as games 
    FROM player_props 
    GROUP BY DATE(commence_time) 
    ORDER BY game_date DESC 
    LIMIT 10
""")

rows = cursor.fetchall()
print("Game dates in database:")
for row in rows:
    print(f"  {row[0]}: {row[1]} games")

print(f"\nToday: {datetime.now().strftime('%Y-%m-%d')}")

# Check most recent scraped data
cursor.execute("""
    SELECT MAX(scraped_at) as last_scrape 
    FROM player_props
""")
last_scrape = cursor.fetchone()[0]
print(f"Last scraped: {last_scrape}")

# Check upcoming games
cursor.execute("""
    SELECT DISTINCT 
        DATE(commence_time) as game_date,
        COUNT(DISTINCT event_id) as games
    FROM player_props
    WHERE DATE(commence_time) >= DATE('now')
    GROUP BY DATE(commence_time)
    ORDER BY game_date ASC
""")
upcoming = cursor.fetchall()
print(f"\nUpcoming games:")
for row in upcoming:
    print(f"  {row[0]}: {row[1]} games")

conn.close()

