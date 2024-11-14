import csv
from tabulate import tabulate
import json
import sys

def print_movies(desired_films):
    
    if not desired_films:
        print("No films found for current filter")
        sys.exit(1)
    
    # sort movies by IMDb rating in descending order
    desired_films.sort(key=lambda x: float(x['imdb_rating']), reverse=True) # display in descending
    
    # prepare data for printing
    headers = ["Title", "Year", "Rating", "Genre", "Runtime", "Director"]
    table = [
        [movie['series_title'], movie['released_year'], movie['imdb_rating'], movie['genre'], movie['runtime'], movie['director']]
        for movie in desired_films
    ]
    
    # print as a table
    print(tabulate(table, headers=headers, tablefmt="plain"))
    return headers

def save_filtered_data(desired_films, headers, file_name=None, file_type=None):
    
    header_to_key_map = {
        "Title": "series_title",
        "Year": "released_year",
        "Rating": "imdb_rating",
        "Genre": "genre",
        "Runtime": "runtime",
        "Director": "director"
    }
    
    if not file_name:
        file_name = "filtered_movies"
    if not file_type:
        file_type = "csv"
    file_path = f"{file_name}.{file_type}"
    
    # align data with headers using the header_to_key_map
    data = [
        {header: movie.get(header_to_key_map[header], '') for header in headers}
        for movie in desired_films
    ]

    if file_type == 'json':
        # save data as JSON
        with open(file_path, mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            
    elif file_type == 'csv':
        # save data as CSV using the helper function
        save_as_csv(file_path, headers, data)
        
    elif file_type in ('plain-text', 'plain', 'txt'):
        # save data as plain text using tabulate
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(tabulate(data, headers=headers, tablefmt="plain"))
        
    else:
        # default to CSV if file type is unsupported
        print(f"Unsupported file type: {file_type}. Defaulting to CSV.")
        save_as_csv(f"{file_name}.csv", headers, data,)

def save_as_csv(file_path, headers, data):
    with open(file_path, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
            