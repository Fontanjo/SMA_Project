# SMA Project

### Carrel Vincent, Corpataux Marine, Fontana Jonas

---

This page contains the code for our Social Media Analytics project. 

During this semester, we implemented a recommender system with multiple different approaches. The idea was to incorporate a social parameter into the classical recommendation, and recommend movies which the user should watch not only because he might like them (high predicted rating), but also because it is "the socially correct thing to watch them", movies which were liked by the popular users in its neighborhood. 

- The matrix decomposition, which is not giving satisfactory results due to a lack of computation capabilities
- User-User CF, with three different weighted:
    - classic model: focus on user-user similarity
    - popularity model: focus on the popularity of the neighbors 
    - hybrid model: a combination of both model above
- Trending now! A prediction of movies to watch, based only on the most popular influencers in the Mubi scene

---

## Prerequisites

- Clone this repository
- Use your favorite package management tool (pipenv, Conda, ...) to install the required dependencies in requirements.txt


## Run the application

- ```$ python main.py```
- Enter the name you want the recommendation for (names are generated randomly at runtime, but one example is always given, and our names are also always added to the dataset)
- Select the method 
- Select the desired visualization (Graph visualization is not available for the method Matrix RS)
- A new window is opened when submitting, you can switch back to the main interface and open a new recommendation to compare the results obtained with the different methods
