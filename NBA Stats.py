from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

# Input for the name
name = input("Enter a player's full name: ")

match = players.find_players_by_full_name(name)

# Exit if player not found
if not match:
    print("Player not found, check spelling")
    exit()

# Get player ID and confirm
player_id = match[0]['id']
print(f"Found: {match[0]['full_name']}")

# Get career stats
career = playercareerstats.PlayerCareerStats(player_id=player_id)
df = career.get_data_frames()[0]

# Calculate 2PT% from made field goals minus three pointers made ; Shot attempts from Field goals attempted minus 3 points attempted
df['2PT_PCT'] = (df['FGM'] - df['FG3M']) / (df['FGA'] - df['FG3A'])
df['2PT_PCT'] = df['2PT_PCT'].round(2)

# Select relevant columns
df_selected = df[['SEASON_ID', 'FG3_PCT', 'FT_PCT', '2PT_PCT']]
df_selected = df_selected.rename(columns={
    'FG3_PCT': '3PT%',
    'FT_PCT': 'FT%',
    'SEASON_ID': 'Season',
    '2PT_PCT': '2PT%'
#Changed names to be easier for users 
})

# Display the data
print('\nShooting Percentages by Season:\n')

print(df_selected.to_string(index=False))
