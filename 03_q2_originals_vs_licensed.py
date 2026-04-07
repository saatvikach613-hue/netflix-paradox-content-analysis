import pandas as pd
import matplotlib.pyplot as plt
import os

OUT = "data/processed/"
PLOTS = "data/processed/plots/"
os.makedirs(PLOTS, exist_ok=True)

df = pd.read_csv(OUT + "netflix_imdb_matched.csv")
df = df.dropna(subset=['averageRating','year_added'])
df = df[df['year_added'].between(2014, 2023)]
df['content_type'] = df['is_original'].map({True: 'Netflix Original', False: 'Licensed Content'})

overall = df.groupby('content_type').agg(
    count=('show_id','count'),
    avg_rating=('averageRating','mean'),
    median_rating=('averageRating','median')
).reset_index()
overall['avg_rating'] = overall['avg_rating'].round(2)

print("=== Q2: ORIGINALS VS LICENSED ===")
print(overall.to_string(index=False))

by_year = df.groupby(['year_added','content_type']).agg(
    count=('show_id','count'),
    avg_rating=('averageRating','mean')
).reset_index()
by_year['avg_rating'] = by_year['avg_rating'].round(2)

orig = overall[overall['content_type'] == 'Netflix Original']
licensed = overall[overall['content_type'] == 'Licensed Content']
if len(orig) > 0 and len(licensed) > 0:
    diff = round(float(orig['avg_rating'].values[0]) - float(licensed['avg_rating'].values[0]), 2)
    print(f"\nOriginals avg: {orig['avg_rating'].values[0]}")
    print(f"Licensed avg:  {licensed['avg_rating'].values[0]}")
    print(f"Difference: {diff} points ({'Originals higher' if diff > 0 else 'Licensed higher'})")

colors = ['#E50914', '#564d4d']
fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='#141414')
for ax in axes:
    ax.set_facecolor('#1f1f1f')

axes[0].bar(overall['content_type'], overall['count'], color=colors, alpha=0.85)
axes[0].set_title('Volume', color='white', fontweight='bold')
axes[0].set_ylabel('Number of Titles', color='white')
axes[0].tick_params(colors='white')
for i, v in enumerate(overall['count']):
    axes[0].text(i, v + 10, str(int(v)), ha='center', fontweight='bold', color='white')

axes[1].bar(overall['content_type'], overall['avg_rating'], color=colors, alpha=0.85)
axes[1].set_title('Avg IMDb Rating', color='white', fontweight='bold')
axes[1].set_ylabel('Average IMDb Rating', color='white')
axes[1].set_ylim(0, 10)
axes[1].tick_params(colors='white')
for i, v in enumerate(overall['avg_rating']):
    axes[1].text(i, v + 0.1, str(round(v, 2)), ha='center', fontweight='bold', color='white')

plt.suptitle('Netflix Originals vs Licensed Content', fontsize=14, fontweight='bold', color='white')
plt.tight_layout()
plt.savefig(PLOTS + "q2_originals_vs_licensed.png", dpi=150, bbox_inches='tight', facecolor='#141414')

overall.to_csv(OUT + "q2_overall_comparison.csv", index=False)
by_year.to_csv(OUT + "q2_by_year.csv", index=False)
print("Saved Q2 CSVs")
