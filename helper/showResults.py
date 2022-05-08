import pandas as pd
import tkinter as tk
from PIL import ImageTk
from urllib.request import urlopen


#Open a window presenting the movies whose ID are given in the list : rank, title, year, predicted ranking, picture


def showResults(recommandation: pd.DataFrame, movie_data: pd.DataFrame):
    movie_data.set_index('movie_id')
    recommanded_movies = recommandation.join(movie_data)

    results = tk.Toplevel()
    results.title("Recommandation")
    labels = []
    images = []
    for count in range(1, 6):
        presentation_text = str(count) + ". " + recommanded_movies.iloc[count-1]["movie_title"] + "\n" + str(int(float(recommanded_movies.iloc[count-1]["movie_release_year"]))) + "\n" + "Predicted rating: " + str(int(float(recommanded_movies.iloc[count-1]["prediction"])))
        labels.append(tk.Label(results, text=presentation_text))
        URL = recommanded_movies.iloc[count-1]["movie_image_url"]
        u = urlopen(URL)
        raw_data = u.read()
        u.close()

        photo = ImageTk.PhotoImage(master=results, data=raw_data)
        photo = photo._PhotoImage__photo.subsample(5)

        images.append(tk.Label(results, image=photo))
        images[len(images)-1].image = photo
    count = 0
    for l in labels:
        l.grid(row=count, column=0)
        count = count+1
    count = 0
    for i in images:
        i.grid(row=count, column=1, pady=2)
        count = count+1

    tk.mainloop()
