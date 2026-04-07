import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

OUT = "data/processed/"
PLOTS = "data/processed/plots/"
os.makedirs(PLOTS, exist_ok=True)

df = pd.read_csv(OUT + "netflix_imdb_matched.csv")
q1 = df.dropna(subset=['year_added','averageRating'])
q1 = q1[q1['year_added'].between(2014, 2023)]

yearly = q1.groupby('year_added').agg(
    title_count=('show_id','count'),
    avg_rating=('averageRating','mean'),
    median_rating=('averageRating','median')
).reset_index()
yearly['avg_rating'] = yearly['avg_rating'].round(2)

print("=== Q1: VOLUME VS QUALITY BY YEAR ===")
print(yearly.to_string(index=False))

peak_rating = yearly['avg_rating'].max()
peak_year = yearly.loc[yearly['avg_rating'].idxmax(), 'year_added']
low_rating = yearly['avg_rating'].min()
low_year = yearly.loc[yearly['avg_rating'].idxmin(), 'year_added']
max_titles = yearly['title_count'].max()
peak_volume_year = yearly.loc[yearly['title_count'].idxmax(), 'year_added']

print(f"\nPeak avg rating: {peak_rating} in {int(peak_year)}")
print(f"Lowest avg rating: {low_rating} in {int(low_year)}")
print(f"Rating drop from peak to trough: {round(peak_rating - low_rating, 2)} points")
print(f"Most titles added: {max_titles} in {int(peak_volume_year)}")

fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(yearly['year_added'], yearly['title_count'], color='#E50914', alpha=0.7, label='Titles Added')
ax1.set_xlabel('Year Added to Netflix', fontsize=12)
ax1.set_ylabel('Number of Titles', color='#E50914', fontsize=12)
ax1.tick_params(axis='y', labelcolor='#E50914')

ax2 = ax1.twinx()
ax2.plot(yearly['year_added'], yearly['avg_rating'], color='white',
         linewidth=2.5, marker='o', markersize=7, label='Avg IMDb Rating')
ax2.set_ylabel('Average IMDb Rating', color='white', fontsize=12)
ax2.tick_params(axis='y', labelcolor='white')
ax2.set_ylim(5, 8)

plt.title('The Netflix Paradox: More Content = Lower Quality?', fontsize=14, fontweight='bold')
fig.patch.set_facecolor('#141414')
ax1.set_facecolor('#1f1f1f')
ax2.set_facecolor('#1f1f1f')
plt.tight_layout()
plt.savefig(PLOTS + "q1_volume_vs_quality.png", dpi=150, bbox_inches='tight', facecolor='#141414')

yearly.to_csv(OUT + "q1_volume_vs_quality.csv", index=False)
print("Saved q1_volume_vs_quality.csv")
