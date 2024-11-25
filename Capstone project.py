import requests
from bs4 import BeautifulSoup as SOUP
import random
import pandas as pd
import os

def fetch_movie_data(genre):

    genre = genre.strip().lower()
    urls = {
        'action': "https://fmovies4free.com/category/action/",
        'comedy': 'https://fmovies4free.com/category/comedy/',
        'drama': 'https://fmovies4free.com/category/drama/',
        'horror': 'https://fmovies4free.com/category/horror/',
        'romance': 'https://fmovies4free.com/category/romance/',
        'sci-fi': 'https://fmovies4free.com/category/sci-fi/'
    }

    urlhere = urls.get(genre)
    if not urlhere:
        print(f"No URL found for the genre: {genre}")
        return []

    response = requests.get(urlhere)
    if response.status_code != 200:
        print(f"Failed to fetch data from URL: {urlhere}")
        return []

    data = response.text
    soup = SOUP(data, 'html.parser')
    titles = soup.find_all("h3", class_="ultp-block-title")
    movie_titles = [title.a.text.strip() for title in titles if title.a]
    return movie_titles

def save_file(movie_list, filename='movies.csv'):
    try:
        df = pd.DataFrame(movie_list, columns =["Movie Title"])
        df.to_csv(filename, index = False)
        print(f"Movies saved to {filename}")
    except Exception as e:
        print("Error while saving the data")

def read_from_file(filename='movies.csv'):
    try:
        if not os.path.exists(filename):
            print(f"File {filename} doesn't exist")
            return []
        df = pd.read_csv(filename)
        return df["Movie Title"].tolist()
    except Exception as e:
        print(f"An error occured while reading from file{e}")


if __name__ == "__main__":
    print("Are you struggling to pick a movie to watch? Come, I'll help you choose one")
    print("Here is a list of Genre you can choose:")
    print("* Action \n* Comedy \n* Drama \n* Horror \n* Romance \n* Sci-Fi")
    choosing_movie = input("Enter the Genre here: ").capitalize()
    movie_list = fetch_movie_data(choosing_movie)

    if movie_list:
        save_file(movie_list)

        movies_from_file = read_from_file()
        if len(movies_from_file) >= 2:
            random_choice = random.sample(movies_from_file, 2)
            print("\nHere are 2 movies you can choose from:\n")
            for movie in random_choice:
                print(movie)

        else:
            print("Oops!, Not enough movies available for this Genre")
    else:
        print("Oops!, No movies available for this Genre")












