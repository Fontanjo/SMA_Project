# SMA_Project

---

## TODOS general

- [ ] Organize work
- [ ] Write small tmux cheat sheet


---

## Done

- [x] Find a way to share data (too big for github)
  - Convert to parquet and split in chunks
- [x] Replace .csv filed with .parquet (and possibly delete unnecessary data)
- [x] Share repo

---


# Structure
Description of all the blocks

## Evaluation

Not included in the project requirement, but very important. Before starting the analytics part (but **after preprocessing**), remove e.g. 10% of the ratings and store them. At the end, predict these ratings.

## Main Component: Network Analytics

**Todo**: Decide algorithm to use. User-user? Item-item? Linear combination? Consider also context-base (see data enrichment)?  
**Todo**: Implement algorithm

## Data Loading

Dataset choosen: https://www.kaggle.com/datasets/clementmsika/mubi-sqlite-database-for-movie-lovers

**Todo**: Describe dataset, why we have choosen it, ...  


## Data Quality and Preprocessing

**Todo**: Describe what and why was removed (useless columns)  
**Todo**: Create methods to upload data  
**Todo**: Preprocess data: remove users with very few ratings
**Todo**: Preprocess data: anomaly detection (possibly in combination with pca)


## Network Exploration

**Todo**: Analyze dataset. Avg ratings per user, per movie, ...  
**Todo**: Find other things to do in this part...


## Graph Storage

**Todo**: Possibly consider other storage than parquet file (can improve accessibility? Speed? Space?)  
**Todo**: Possibly describe why .parquet (speed, space)


## Network Visualization

**Todo**: Find useful relations to visualize  
**Todo**: Find a way to show these relations  
**Todo**: Possibly find a nice way to visualize output


## Data Enrichment

**Todo**: Consider if necessary. Since we have the movies names, we could find external descriptions, and use them to combine out main algorithm with some context-base recommender system

---


# Dependencies
List of libraries and min. version
