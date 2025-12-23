"""
Test the date filtering logic to see what's happening
"""

import sqlite3
from datetime import datetime, timedelta, timezone

# Find database
DB_PATH = 'data/odds_data.db'

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("="*70)
print("DATE FILTERING TEST")
print("="*70)

# Get current UTC time
now_utc = datetime.now(timezone.utc)
print(f"\nCurrent UTC time: {now_utc}")
print(f"Current UTC ISO: {now_utc.isoformat()}")

# Get all games
cursor.execute("""
    SELECT DISTINCT
        event_id,
        home_team,
        away_team,
        commence_time
    FROM player_props
    ORDER BY commence_time
""")
games = cursor.fetchall()

print(f"\n\nAll {len(games)} games in database:")
print("-"*70)
for i, game in enumerate(games, 1):
    game_time_str = game['commence_time']
    # Parse the game time
    game_time = datetime.fromisoformat(game_time_str.replace('Z', '+00:00'))
    
    # Calculate difference from now
    time_diff = game_time - now_utc
    hours_until = time_diff.total_seconds() / 3600
    
    print(f"\n{i}. {game['away_team']} @ {game['home_team']}")
    print(f"   Commence: {game_time_str}")
    print(f"   Parsed:   {game_time}")
    print(f"   Hours from now: {hours_until:.1f} hours")
    
    # Categorize
    if hours_until < 0:
        print(f"   STATUS: PAST (already started)")
    elif hours_until < 24:
        print(f"   STATUS: TODAY (next 24 hours)")
    elif hours_until < 48:
        print(f"   STATUS: TOMORROW (24-48 hours)")
    else:
        print(f"   STATUS: FUTURE (>48 hours)")

# Test TODAY filter
print("\n\n" + "="*70)
print("TESTING 'TODAY' FILTER")
print("="*70)
start_of_day = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_day = now_utc.replace(hour=23, minute=59, second=59, microsecond=999999)

print(f"Start of today (UTC): {start_of_day.isoformat()}")
print(f"End of today (UTC): {end_of_day.isoformat()}")

condition = f"commence_time >= '{start_of_day.isoformat()}' AND commence_time <= '{end_of_day.isoformat()}' AND commence_time > '{now_utc.isoformat()}'"
print(f"\nSQL condition: {condition}\n")

cursor.execute(f"""
    SELECT DISTINCT event_id, home_team, away_team, commence_time
    FROM player_props
    WHERE {condition}
    ORDER BY commence_time
""")
today_games = cursor.fetchall()
print(f"Games matching 'TODAY': {len(today_games)}")
for game in today_games:
    print(f"  - {game['away_team']} @ {game['home_team']} ({game['commence_time']})")

# Test TOMORROW filter
print("\n\n" + "="*70)
print("TESTING 'TOMORROW' FILTER")
print("="*70)
start_of_tomorrow = (now_utc + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
end_of_tomorrow = start_of_tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)

print(f"Start of tomorrow (UTC): {start_of_tomorrow.isoformat()}")
print(f"End of tomorrow (UTC): {end_of_tomorrow.isoformat()}")

condition = f"commence_time >= '{start_of_tomorrow.isoformat()}' AND commence_time <= '{end_of_tomorrow.isoformat()}' AND commence_time > '{now_utc.isoformat()}'"
print(f"\nSQL condition: {condition}\n")

cursor.execute(f"""
    SELECT DISTINCT event_id, home_team, away_team, commence_time
    FROM player_props
    WHERE {condition}
    ORDER BY commence_time
""")
tomorrow_games = cursor.fetchall()
print(f"Games matching 'TOMORROW': {len(tomorrow_games)}")
for game in tomorrow_games:
    print(f"  - {game['away_team']} @ {game['home_team']} ({game['commence_time']})")

# Test WEEK filter
print("\n\n" + "="*70)
print("TESTING 'WEEK' FILTER")
print("="*70)
week_from_now = now_utc + timedelta(days=7)

print(f"Now (UTC): {now_utc.isoformat()}")
print(f"Week from now (UTC): {week_from_now.isoformat()}")

condition = f"commence_time >= '{now_utc.isoformat()}' AND commence_time <= '{week_from_now.isoformat()}' AND commence_time > '{now_utc.isoformat()}'"
print(f"\nSQL condition: {condition}\n")

cursor.execute(f"""
    SELECT DISTINCT event_id, home_team, away_team, commence_time
    FROM player_props
    WHERE {condition}
    ORDER BY commence_time
""")
week_games = cursor.fetchall()
print(f"Games matching 'WEEK': {len(week_games)}")
for game in week_games:
    print(f"  - {game['away_team']} @ {game['home_team']} ({game['commence_time']})")

print("\n" + "="*70)
print("DIAGNOSIS")
print("="*70)

# Show what's in each bucket
print(f"\nTODAY: {len(today_games)} games")
print(f"TOMORROW: {len(tomorrow_games)} games")
print(f"WEEK: {len(week_games)} games")

if len(today_games) == len(tomorrow_games) == len(week_games):
    print("\n⚠️  PROBLEM: All filters return the same games!")
    print("This means the date filtering logic isn't working correctly.")
    
    # Show why
    print("\nLet's check the actual game times:")
    for game in games:
        game_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
        print(f"\n{game['home_team']} vs {game['away_team']}")
        print(f"  Game time: {game_time}")
        print(f"  Now:       {now_utc}")
        print(f"  Start of today:    {start_of_day}")
        print(f"  End of today:      {end_of_day}")
        print(f"  Start of tomorrow: {start_of_tomorrow}")
        print(f"  End of tomorrow:   {end_of_tomorrow}")
        
        # Check each condition
        in_today = start_of_day <= game_time <= end_of_day and game_time > now_utc
        in_tomorrow = start_of_tomorrow <= game_time <= end_of_tomorrow and game_time > now_utc
        
        print(f"  In today range? {in_today}")
        print(f"  In tomorrow range? {in_tomorrow}")

conn.close()