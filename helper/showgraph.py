import networkx as nx
from networkx import bipartite
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#display a window with the recommandation as a graph

def showgraph(ratings, recommandation, movie_data):

    data = ratings.to_dict(orient='records')
    recomm, similarity = recommandation
    movies = movie_data.copy()
    movies.set_index('movie_id', inplace=True, drop=True)

    G = nx.Graph()

    for row in data:
        if row["user_id"] in list(similarity.columns) and row["movie_id"] in recomm.index.to_list():
            if row["movie_id"] not in G:
                G.add_node(row["movie_id"], value="movie", color="grey", prediction=round(recomm.loc[row["movie_id"]]['prediction'],2),
                           title=movies.loc[row["movie_id"]]['movie_title'], bipartite=0)
            if row["user_id"] not in G:
                G.add_node(row["user_id"], value="user", color="black", bipartite=1)
            if row["rating_score"] == 1:
                G.add_edge((row["movie_id"]), (row["user_id"]), rate=row["rating_score"], color="yellow")
            elif row["rating_score"] == 2:
                G.add_edge((row["movie_id"]), (row["user_id"]), rate=row["rating_score"], color="orange")
            elif row["rating_score"] == 3:
                G.add_edge((row["movie_id"]), (row["user_id"]), rate=row["rating_score"], color="red")
            elif row["rating_score"] == 4:
                G.add_edge((row["movie_id"]), (row["user_id"]), rate=row["rating_score"], color="purple")
            elif row["rating_score"] == 5:
                G.add_edge((row["movie_id"]), (row["user_id"]), rate=row["rating_score"], color="blue")


    node_color = nx.get_node_attributes(G,'color').values()
    edge_color = nx.get_edge_attributes(G, 'color').values()


    fig = plt.figure("Graph representation", figsize=(10, 10))
    # Create a gridspec for adding subplots of different sizes
    axgrid = fig.add_gridspec(1, 1)

    ax = fig.add_subplot(axgrid[:, :])
    X, Y = bipartite.sets(G)
    pos = nx.drawing.layout.bipartite_layout(G, Y)
    nx.draw(G, pos=pos, node_color=node_color, edge_color=edge_color)
    labels_pred = nx.get_node_attributes(G, 'prediction')
    nx.draw_networkx_labels(G, pos, labels=labels_pred, font_size=8, horizontalalignment='center', verticalalignment='center')
    labels_title = nx.get_node_attributes(G, 'title')
    pos_attrs = {}
    for node, coords in pos.items():
        pos_attrs[node] = (coords[0], coords[1] + 0.04)
    nx.draw_networkx_labels(G, pos_attrs, labels=labels_title, font_size=8)
    ax.set_title("Movies and users")
    ax.set_axis_off()

    yellow_patch = mpatches.Patch(color='yellow', label='rate = 1')
    orange_patch = mpatches.Patch(color='orange', label='rate = 2')
    red_patch = mpatches.Patch(color='red', label='rate = 3')
    purple_patch = mpatches.Patch(color='purple', label='rate = 4')
    blue_patch = mpatches.Patch(color='blue', label='rate = 5')
    black_patch = mpatches.Patch(color='grey', label='movies')
    grey_patch = mpatches.Patch(color='black', label='users')
    plt.legend(handles=[yellow_patch, orange_patch, red_patch, purple_patch, blue_patch, black_patch, grey_patch], loc=9, fontsize='small')

    fig.tight_layout()
    plt.show()
