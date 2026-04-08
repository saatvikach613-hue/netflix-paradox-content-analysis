import pandas as pd
import numpy as np
import os

RAW = "data/raw/"
OUT = "data/processed/"
os.makedirs(OUT, exist_ok=True)

print("Loading Netflix data...")
netflix = pd.read_csv(RAW + "netflix_titles.csv")
netflix = netflix[['show_id','type','title','director','country',
                   'date_added','release_year','rating','listed_in','description']]

netflix['title_clean'] = (netflix['title']
                          .str.lower().str.strip()
                          .str.replace(r'[^a-z0-9\s]', '', regex=True).str.strip())

netflix['date_added'] = pd.to_datetime(netflix['date_added'], errors='coerce')
netflix['year_added'] = netflix['date_added'].dt.year
netflix['release_year'] = pd.to_numeric(netflix['release_year'], errors='coerce')

netflix['is_original'] = netflix['release_year'] == netflix['year_added']

print(f"Netflix: {netflix.shape[0]} titles loaded")

print("Loading IMDb basics (this takes a minute)...")
imdb_basics = pd.read_csv(RAW + "title.basics.tsv", sep='\t', na_values='\\N',
                           usecols=['tconst','titleType','primaryTitle','startYear'],
                           low_memory=False)
imdb_basics = imdb_basics[imdb_basics['titleType'].isin(['movie','tvSeries','tvMiniSeries'])]
imdb_basics['title_clean'] = (imdb_basics['primaryTitle']
                               .str.lower().str.strip()
                               .str.replace(r'[^a-z0-9\s]', '', regex=True).str.strip())

print("Loading IMDb ratings...")
imdb_ratings = pd.read_csv(RAW + "title.ratings.tsv", sep='\t', na_values='\\N')

imdb = imdb_basics.merge(imdb_ratings, on='tconst', how='inner')

print("Merging Netflix + IMDb on title name...")
merged = netflix.merge(
    imdb[['title_clean','averageRating','numVotes','startYear']],
    on='title_clean', how='left')
merged = merged.sort_values('numVotes', ascending=False)
merged = merged.drop_duplicates(subset=['show_id'], keep='first')

matched = merged.dropna(subset=['averageRating'])
print(f"Matched: {len(matched)} of {len(netflix)} titles ({len(matched)/len(netflix)*100:.1f}%)")

merged.to_csv(OUT + "netflix_imdb_merged.csv", index=False)
matched.to_csv(OUT + "netflix_imdb_matched.csv", index=False)
print("Saved. Run Script 02 next.")
