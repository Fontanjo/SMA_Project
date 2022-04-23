import pandas as pd
import tkinter as tk
from PIL import ImageTk
from urllib.request import urlopen


#Open a window presenting the movies whose ID are given in the list : rank, title, year, picture
#list should be a list of integers corresponding to the ID of the movies, ranked in preference order (first is the best)


def showResults(list):
    recommanded = [0,0,0,0,0]
    doc = pd.read_parquet("mubi_movie_data.parquet")
    doc = doc.to_dict(orient='records')
    for row in doc:
        if len(list) >= 1 and row["movie_id"] == list[0]:
            recommanded[0] = row
        if len(list) >= 2 and row["movie_id"] == list[1]:
            recommanded[1] = row
        if len(list) >= 3 and row["movie_id"] == list[2]:
            recommanded[2] = row
        if len(list) >= 4 and row["movie_id"] == list[3]:
            recommanded[3] = row
        if len(list) >= 5 and row["movie_id"] == list[4]:
            recommanded[4] = row

    results = tk.Tk()
    labels = []
    images = []
    count = 1
    for r in recommanded:
        if r != 0:
            labels.append(tk.Label(results, text=str(count) + ". " + r["movie_title"] + "\n" + str(int(float(r["movie_release_year"])))))
            count = count + 1
            URL = r["movie_image_url"]
            u = urlopen(URL)
            raw_data = u.read()
            u.close()

            photo = ImageTk.PhotoImage(data=raw_data)
            photo = photo._PhotoImage__photo.subsample(5)

            images.append(tk.Label(image=photo))
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
