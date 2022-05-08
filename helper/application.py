import tkinter as tk
import collaborative
import loader
import preprocesser
import showresults as show

#IF YOU WANT TO TEST APPLICATION, YOU CAN USE USER ID 2941

def application():
    
    
    #definition of the function happening when "Submit" button is hit
    def algorithm():

        #get the user from the user field
        user = int(entry.get("1.0",'end-1c'))
        if user not in dense_user_item.index:
            error_text.set("The user " + str(user) + " doesn't exist!")
            return

        #get the recommander algorithm from the listbox
        selection = type.curselection()
        if len(selection)==0:
            error_text.set("Please select an algorithm")
            return
        index = selection[0]
        value = type.get(index)

        #Show error if Matric RS is requested
        if value == "Matrix RS":
            error_text.set("Matrix RS algorithm isn't working yet")
            return

        #select the right algorithm according to the selected value in the listbox and print the page
        if value == "Classic RS":
            error_text.set("")
            recomm_classic = collaborative.classic_RS(user, dense_user_item, neighboor_size=100, top_K=30, norm=True)
            recomm_classic.transpose()
            show.showResults(recomm_classic, movies)
        elif value == "Hybrid RS":
            error_text.set("")
            recomm_hybdrid = collaborative.hybdrid_RS(user, dense_user_item, popu_matrix, neighboor_size=100, top_K=30,
                                                      norm=True)
            recomm_hybdrid.transpose()
            show.showResults(recomm_hybdrid, movies)
        elif value == "Popularity RS":
            error_text.set("")
            recomm_pop = collaborative.popularity_RS(user, dense_user_item, popu_matrix, neighboor_size=100, top_K=30,
                                                     norm=True)
            recomm_pop.transpose()
            show.showResults(recomm_pop, movies)

    #Loading, preprocessing
    ratings = loader.load_ratings()
    movies = loader.load_movies()
    lists = loader.load_lists()
    ratings_new, lists_new = preprocesser.preprocess_ratings(ratings, lists, 500)
    dense_user_item = collaborative.get_dense_user_item(ratings_new)
    popu_matrix = collaborative.get_popularity(lists_new, dense_user_item)

    #Create the window
    root = tk.Tk()
    root.title("Interface")

    # Create box of texts
    entry = tk.Text(root, height=1, width=52)
    Entry = """Type a name"""
    type = tk.Listbox(root, height=4, width=52)
    error_text = tk.StringVar()
    error = tk.Label(root, textvariable=error_text, fg="red", height=1, width=52)
    title = tk.Label(root, text="Who do you want a recommandation for?")
    title.config(font=("Courier", 14))

    # Create button to submit
    b1 = tk.Button(root, text="Submit", width=30, command=algorithm)

    # Create button to exit
    b2 = tk.Button(root, text="Exit", width=30, command=root.destroy)

    #Place elements on the window
    title.grid(row=1, columnspan=2)
    entry.grid(row=2, columnspan=2)
    type.grid(row=3, columnspan=2)
    error.grid(row=4, columnspan=2)
    b1.grid(row=5, column=0)
    b2.grid(row=5, column=1)

    #Insert texts
    entry.insert(tk.END, "Type a name")
    type.insert(tk.END, "Classic RS")
    type.insert(tk.END, "Hybrid RS")
    type.insert(tk.END, "Popularity RS")
    type.insert(tk.END, "Matrix RS")
    
    #show window
    tk.mainloop()
