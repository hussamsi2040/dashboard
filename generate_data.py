import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

def generate_gaming_dataset(n_players=10000):
    """
    Generate a comprehensive gaming behavior dataset with monetization and retention metrics
    
    Parameters:
    n_players (int): Number of players to generate
    """
    
    # Define possible values for categorical variables
    game_genres = ['Action RPG', 'Strategy', 'Casual', 'Puzzle', 'Adventure', 'Sports', 'Battle Royale']
    difficulties = ['Kolay', 'Orta', 'Zor']  # Turkish difficulty levels
    engagement_levels = ['Düşük', 'Orta', 'Yüksek']  # Turkish engagement levels
    locations = ['Türkiye', 'ABD', 'Almanya', 'İngiltere', 'Fransa', 'Rusya', 'Japonya', 'Güney Kore', 'Diğer']
    genders = ['Erkek', 'Kadın', 'Diğer']  # Turkish gender labels
    devices = ['Android', 'iOS', 'PC', 'Console']
    
    # Generate base data
    current_date = datetime.now()
    signup_dates = [current_date - timedelta(days=np.random.randint(1, 365)) for _ in range(n_players)]
    
    data = {
        'PlayerID': np.arange(9000, 9000 + n_players),
        'Age': np.clip(np.random.normal(28, 8, n_players), 18, 65).astype(int),
        'Gender': np.random.choice(genders, n_players, p=[0.65, 0.30, 0.05]),
        'Location': np.random.choice(locations, n_players),
        'Device': np.random.choice(devices, n_players),
        'SignupDate': signup_dates,
        'GameGenre': np.random.choice(game_genres, n_players),
        'GameDifficulty': np.random.choice(difficulties, n_players, p=[0.3, 0.5, 0.2])
    }
    
    # --- Add A/B Test Group Assignment ---
    data['AB_Group'] = np.random.choice(['A', 'B'], n_players)
    # -------------------------------------
    
    # Generate monetization metrics
    data['HasPurchased'] = np.random.choice([0, 1], n_players, p=[0.85, 0.15])
    purchase_amounts = np.zeros(n_players)
    purchasers = data['HasPurchased'] == 1
    purchase_amounts[purchasers] = np.random.gamma(2, 15, purchasers.sum())
    data['TotalSpentUSD'] = purchase_amounts.round(2)
    
    # --- Simulate small uplift for Group B on spending ---
    group_b_purchasers = (data['AB_Group'] == 'B') & purchasers
    uplift_amount = np.random.uniform(0.5, 5, group_b_purchasers.sum()) # Small random uplift
    data['TotalSpentUSD'][group_b_purchasers] += uplift_amount.round(2)
    # Ensure no negative spending if base was 0 (though unlikely here)
    data['TotalSpentUSD'] = np.maximum(0, data['TotalSpentUSD'])
    # ---------------------------------------------------
    
    # Generate engagement metrics
    base_play_time = np.random.gamma(2, 5, n_players)
    age_factor = 1 - (data['Age'] - 25) * 0.01
    difficulty_factor = pd.Series(data['GameDifficulty']).map({
        'Kolay': 0.8,
        'Orta': 1.0,
        'Zor': 1.2
    })
    data['PlayTimeHours'] = (base_play_time * age_factor * difficulty_factor).round(2)
    
    # Session metrics
    data['SessionsPerWeek'] = np.clip(
        np.random.normal(8, 3, n_players) * (data['PlayTimeHours'] / data['PlayTimeHours'].mean()) * 0.8,
        1, 30
    ).astype(int)
    
    data['AvgSessionDurationMinutes'] = np.clip(
        (data['PlayTimeHours'] * 60 / data['SessionsPerWeek']) * np.random.normal(1, 0.1, n_players),
        15, 240
    ).round(0).astype(int)
    
    # Progression metrics
    data['PlayerLevel'] = np.clip(
        data['PlayTimeHours'] * np.random.normal(5, 1, n_players) * 
        pd.Series(data['GameDifficulty']).map({'Kolay': 1.2, 'Orta': 1.0, 'Zor': 0.8}),
        1, 100
    ).astype(int)
    
    # Achievement and completion metrics
    max_achievements = 50
    achievement_base = (data['PlayerLevel'] / 100) * (data['PlayTimeHours'] / data['PlayTimeHours'].max())
    data['AchievementsUnlocked'] = np.clip(
        achievement_base * max_achievements * np.random.normal(1, 0.2, n_players),
        0, max_achievements
    ).astype(int)
    
    # Retention metrics
    days_since_signup = [(current_date - date).days for date in signup_dates]
    data['DaysSinceSignup'] = days_since_signup
    
    retention_prob = np.clip(0.9 - np.array(days_since_signup) * 0.001, 0.1, 0.9)
    data['IsActive'] = np.random.binomial(1, retention_prob)
    data['LastActiveDate'] = [
        current_date - timedelta(days=np.random.randint(0, 7) if is_active else np.random.randint(30, 365))
        for is_active in data['IsActive']
    ]
    
    # Social metrics
    data['FriendsCount'] = np.random.poisson(5, n_players)
    data['GuildMember'] = np.random.choice([0, 1], n_players, p=[0.7, 0.3])
    
    # Performance metrics
    data['AvgFPS'] = np.clip(np.random.normal(55, 10, n_players), 30, 60).round(1)
    data['CrashCount'] = np.random.poisson(0.5, n_players)
    
    # Generate engagement level based on multiple factors
    play_time_normalized = (data['PlayTimeHours'] - data['PlayTimeHours'].min()) / (data['PlayTimeHours'].max() - data['PlayTimeHours'].min())
    achievements_normalized = data['AchievementsUnlocked'] / max_achievements
    purchase_normalized = (data['TotalSpentUSD'] - data['TotalSpentUSD'].min()) / (data['TotalSpentUSD'].max() - data['TotalSpentUSD'].min())
    
    engagement_score = (play_time_normalized + achievements_normalized + purchase_normalized) / 3
    data['EngagementLevel'] = pd.qcut(engagement_score, q=3, labels=engagement_levels)
    
    # Create DataFrame and sort by PlayerID
    df = pd.DataFrame(data)
    df = df.sort_values('PlayerID')
    
    return df

if __name__ == "__main__":
    # Generate dataset
    n_players = 10000
    df = generate_gaming_dataset(n_players)
    
    # Save to CSV
    output_file = 'data/online_gaming_behavior_dataset.csv'
    df.to_csv(output_file, index=False)
    print(f"Generated dataset with {n_players} players and saved to {output_file}")
    
    # Display statistics in Turkish
    print("\nVeri Seti İstatistikleri:")
    print("-" * 50)
    print(f"Toplam Oyuncu: {len(df):,}")
    print(f"Ortalama Oynama Süresi: {df['PlayTimeHours'].mean():.2f} saat")
    print(f"Ortalama Oyuncu Seviyesi: {df['PlayerLevel'].mean():.1f}")
    print(f"Haftalık Ortalama Oturum: {df['SessionsPerWeek'].mean():.1f}")
    print(f"Toplam Gelir: ${df['TotalSpentUSD'].sum():,.2f}")
    
    print("\nKatılım Seviyesi Dağılımı:")
    print(df['EngagementLevel'].value_counts())
    
    print("\nOyun Türü Dağılımı:")
    print(df['GameGenre'].value_counts()) 