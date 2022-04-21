import pandas as pd
import os


def load_ratings():
    # Save current working directory to restore at the end (TODO check if necessary)
    current_wd = os.getcwd()
    # Move working directory tho this file location
    try:
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
    except Exception as e:
        print('Error in changing working directory, data might not be loaded correctly')
    # Load first part
    ratings_data_reduced0 = pd.read_parquet('../mubi_ratings_data_0.parquet')
    # Load second part
    ratings_data_reduceda = pd.read_parquet('../mubi_ratings_data_1.parquet')
    # Merge data
    ratings_data = pd.concat([ratings_data_reduced0, ratings_data_reduced1])
    # Restore original working directory
    os.chdir(current_wd)
    # Return DataFrame
    return ratings_data


def load_movies():
    # Save current working directory to restore at the end (TODO check if necessary)
    current_wd = os.getcwd()
    # Move working directory tho this file location
    try:
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
    except Exception as e:
        print('Error in changing working directory, data might not be loaded correctly')
    # Load data
    movie_data = pd.read_parquet('../mubi_movie_data.parquet')
    # Restore original working directory
    os.chdir(current_wd)
    # Return DataFrame
    return movie_data


def load_lists():
    # Save current working directory to restore at the end (TODO check if necessary)
    current_wd = os.getcwd()
    # Move working directory tho this file location
    try:
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
    except Exception as e:
        print('Error in changing working directory, data might not be loaded correctly')
    # Load data
    list_data = pd.read_parquet('../mubi_lists_data.parquet')
    # Restore original working directory
    os.chdir(current_wd)
    # Return DataFrame
    return list_data
