import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

OUT = "data/processed/"
PLOTS = "data/processed/plots/"
os.makedirs(PLOTS, exist_ok=True)

df = pd.read_csv(OUT + "netflix_imdb_matched.csv")
df = df.dropna(subset=['averageRating','listed_in'])

df['genres'] = df['listed_in'].str.split(',')
df_genres = df.explode('genres')
df_genres['genres'] = df_genres['genres'].str.strip()

genre_stats = df_genres.groupby('genres').agg(
    title_count=('show_id','count'),
    avg_rating=('averageRating','mean'),
    median_rating=('averageRating','median')
).reset_index()
genre_stats['avg_rating'] = genre_stats['avg_rating'].round(2)

# Your invented metric
genre_stats['content_efficiency_score'] = (
    genre_stats['avg_rating'] * np.log(genre_stats['title_count'])).round(2)

genre_stats = genre_stats[genre_stats['title_count'] >= 20].copy()
genre_stats = genre_stats.sort_values('content_efficiency_score', ascending=False)

print("=== Q3: GENRE SATURATION ===")
print(genre_stats.to_string(index=False))

median_vol = genre_stats['title_count'].median()
median_rate = genre_stats['avg_rating'].median()

def quadrant(row):
    if row['title_count'] >= median_vol and row['avg_rating'] >= median_rate:
        return "Sweet Spot"
    elif row['title_count'] < median_vol and row['avg_rating'] >= median_rate:
        return "Underloved"
    elif row['title_count'] >= median_vol and row['avg_rating'] < median_rate:
        return "Oversaturated"
    else:
        return "Dead Zone"

genre_stats['quadrant'] = genre_stats.apply(quadrant, axis=1)
print("\nQuadrant breakdown:")
print(genre_stats.groupby('quadrant')['genres'].apply(list))

color_map = {
    "Sweet Spot": "#4ade80",
    "Underloved": "#60a5fa",
    "Oversaturated": "#e74c3c",
    "Dead Zone": "#6b7280"
}

fig, ax = plt.subplots(figsize=(14, 9), facecolor='#141414')
ax.set_facecolor('#1a1a2e')

for quad, color in color_map.items():
    subset = genre_stats[genre_stats['quadrant'] == quad]
    ax.scatter(subset['title_count'], subset['avg_rating'],
               c=color, s=subset['content_efficiency_score'] * 3,
               alpha=0.8, label=quad, edgecolors='white', linewidth=0.5)
    for _, row in subset.iterrows():
        ax.annotate(row['genres'], (row['title_count'], row['avg_rating']),
                    fontsize=7.5, ha='center', va='bottom', color='white',
                    xytext=(0, 5), textcoords='offset points')

ax.axvline(median_vol, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.axhline(median_rate, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.set_xlabel('Number of Titles (Volume)', fontsize=12, color='white')
ax.set_ylabel('Average IMDb Rating (Quality)', fontsize=12, color='white')
ax.set_title('Netflix Genre Saturation Map — Volume vs Quality',
             fontsize=14, fontweight='bold', color='white', pad=15)
ax.legend(loc='upper right', fontsize=9)
ax.tick_params(colors='white')
ax.grid(alpha=0.15)
plt.tight_layout()
plt.savefig(PLOTS + "q3_genre_saturation.png", dpi=150, bbox_inches='tight', facecolor='#141414')

genre_stats.to_csv(OUT + "q3_genre_saturation.csv", index=False)
print("Saved q3_genre_saturation.csv")
print("\nTop 10 by Content Efficiency Score:")
print(genre_stats[['genres','title_count','avg_rating','content_efficiency_score','quadrant']].head(10).to_string(index=False))
