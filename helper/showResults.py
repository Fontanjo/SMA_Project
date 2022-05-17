import pandas as pd
import tkinter as tk
from PIL import ImageTk
from urllib.request import urlopen


#Open a window presenting the movies whose ID are given in the list : rank, title, year, predicted ranking, picture


def showResults(recommandation: pd.DataFrame, movie_data: pd.DataFrame):
    showed_results = 10 #this number can be changed and the displayer will adapt
    movies = movie_data.copy()
    movies.set_index('movie_id',inplace=True, drop=True)
    recommanded_movies = recommandation.join(movies)

    results = tk.Toplevel()
    results.title("Recommandation")
    labels = []
    images = []
    for count in range(1, showed_results + 1):
        presentation_text = str(count) + ". " + recommanded_movies.iloc[count-1]["movie_title"] + "\n" + str(int(float(recommanded_movies.iloc[count-1]["movie_release_year"]))) + "\n" + "Predicted rating: " + str(round(float(recommanded_movies.iloc[count-1]["prediction"]),2))
        labels.append(tk.Label(results, text=presentation_text))
        URL = recommanded_movies.iloc[count-1]["movie_image_url"]
        u = urlopen(URL)
        raw_data = u.read()
        u.close()

        photo = ImageTk.PhotoImage(master=results, data=raw_data)
        photo = photo._PhotoImage__photo.subsample(5)

        images.append(tk.Label(results, image=photo))
        images[len(images)-1].image = photo
        
    count_row = 0
    count_column = 0
    for l in labels:
        l.grid(row=count_row, column=count_column)
        count_row = count_row+1
        if count_row == 5:
            count_column = count_column + 2
            count_row = 0
            
    count_row = 0
    count_column = 1
    for i in images:
        i.grid(row=count_row, column=count_column, pady=2)
        count_row = count_row + 1
        if count_row == 5:
            count_column = count_column + 2
            count_row = 0

    tk.mainloop()
