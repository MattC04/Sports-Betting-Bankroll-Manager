import requests
import json

# Test the API endpoint
try:
    response = requests.get('http://localhost:5000/api/games?sport=basketball_nba&date=week')
    data = response.json()
    
    print(f"Success: {data.get('success')}")
    print(f"Games count: {data.get('count', 0)}")
    print(f"\nGames returned:")
    for game in data.get('games', [])[:5]:
        print(f"  - {game.get('away_team')} @ {game.get('home_team')}")
        print(f"    Time: {game.get('commence_time')}")
        print(f"    Date: {game.get('commence_time', '')[:10]}")
        print()
except Exception as e:
    print(f"Error: {e}")
    print("\nMake sure the dashboard server is running:")
    print("  python dashboard.py")

