# 🍿 The Netflix Paradox: Content Strategy & Quality Analysis

**Tableau Dashboard Visualization:** [Netflix Content Strategy Analysis](https://public.tableau.com/app/profile/saatvika.chokkapu/viz/NetflicContentStrategyAnalysis/NetflixContentStrategyAnalysis)

## 📌 What Are We Trying to Achieve?

From 2015 to 2024, Netflix's content library underwent an explosive expansion, scaling from roughly 5,000 titles to over 36,000 worldwide. They now spend approximately $17 billion annually on content alone. This aggressive "Originals" pipeline and mass licensing approach led to an important industry question that has rarely been backed by quantitative data: **Did adding more content actually make the Netflix catalog better, or did the quality plummet as volume exploded?**
The primary objective of this project was to answer that question empirically. By engineering a custom data pipeline to bridge Netflix's catalog with public IMDb ratings, we set out to analyze the true tradeoff between content volume and critical acclaim. 
### **Success Criteria**
The project was considered successful by fulfilling three core analysis milestones:
1. Identifying if, and exactly when, average content quality started to drop due to catalog expansion.
2. Determining whether the massive $17 Billion "Originals" strategy is actually yielding higher quality content than simply licensing existing work.
3. Calculating genre saturation explicitly, grouping Netflix's entire catalog into quantifiable "Sweet Spots", "Oversaturated" zones, and "Dead Zones" using a newly invented KPI (*Content Efficiency Score*).

---

## 🛠 Project Data & Architecture
To measure accurate acclaim, we couldn't rely on a single flat file. We had to perform data pipeline engineering by merging two wildly different public datasets:
- **Dataset 1**: Kaggle's Netflix Titles Dataset (netflix_titles.csv) containing metadata (Release Year, Cast, Director, Genre).
- **Dataset 2 & 3**: IMDb's massive public relations tables (title.basics.tsv and title.ratings.tsv) containing standardized global user ratings. 
**The Pipeline Challenge:** 
The IMDb datasets have zero Netflix tracking, and Netflix's dataset has no numerical ratings. The first script of the architecture parses through both databases, cleans string punctuations to normalize title strings, performs an inner join via pandas on matching titles, and drops duplicates to create one unified master dataframe (netflix_imdb_merged.csv). 
### Tech Stack
- **Data Engineering:** Python, Pandas, Numpy.
- **Visualization (Exploratory):** Matplotlib, Seaborn.
- **Visualization (Production):** Tableau Public.
---
## 🔍 The 3 Key Questions Answered (Methodology & Results)
### Q1: Does More Content = Worse Quality? (The Volume vs. Quality Paradox)
We aggregated all matched titles by the year they were added to Netflix, calculating both total volume and average IMDb rating per year. 
**Results:**
- **Peak Quality:** Netflix's catalog had an impressive average IMDb rating of **7.35 in 2014**, when the platform was heavily curated and volume was low.
- **The Drop:** As volume skyrocketed from hundreds of titles to roughly **1,624 titles added in 2019**, the average rating hit a trough, stabilizing at roughly **6.44 - 6.50**. 
- **Conclusion:** There is a clear inversely proportional relationship between Netflix's volume explosion and critical quality. 
### Q2: Is the $17 Billion "Originals" Strategy Actually Working?
Using a proxy algorithm (where independent titles released in the same year they are added to Netflix are marked as Originals), we segregated the catalog to compare Netflix Originals against third-party "Licensed Content".
**Results:**
- **Licensed Content:** Historically dominates the higher ratings with a **6.60 average IMDb score** across roughly 3,990 titles.
- **Netflix Originals:** Hit a lower **6.36 average IMDb score** across 2,865 titles. 
- **Conclusion:** While Originals represent a strategic moat for subscriber retention, they are empirically lower in critical acclaim than the premium licensed movies and shows Netflix pays to house.
### Q3: Which Genres are Oversaturated? (Content Efficiency Score)
To determine true content gaps, we created a custom KPI called **Content Efficiency Score**: Average IMDb Rating × log(Number of Titles). This statistically rewards high-quality curation acting at scale while punishing low-rated bloat.
By plotting average rating against total volume and splitting the graph at the median values, we established four clear Quadrants:
1. 🟢 **Sweet Spot (High Volume, High Rating):** Documentaries, TV Dramas, International TV Shows, and Crime TV Shows. 
2. 🔵 **Underloved (Low Volume, High Rating):** Anime Series, Korean TV Shows, Classic & Cult TV. (Huge potential for safe investment).
3. 🔴 **Oversaturated (High Volume, Low Rating):** Dramas, Comedies, and International Movies. (Too much bloat bringing down average platform ratings).
4. ⚪ **Dead Zone (Low Vol, Low Rating):** Sci-Fi, Horror Movies.
---
## 🚀 How to Run the Pipeline
If you would like to rebuild the matching arrays and visualizations yourself:
1. Clone or download this repository.
2. Put the netflix_titles.csv file inside data/raw/. 
3. Run the pipeline shell script or python files in scripts/:
   bash
   pip install pandas numpy matplotlib seaborn
   python scripts/01_clean_and_merge.py
   python scripts/02_q1_volume_vs_quality.py
   python scripts/03_q2_originals_vs_licensed.py
   python scripts/04_q3_genre_saturation.py
   
4. Output datasets will cleanly export to data/processed/, ready for direct Tableau injection. 
---
*Created as a comprehensive portfolio project demonstrating Data Engineering, Pandas Merge Operations, Exploratory Data Analysis, and KPI strategy development.*
