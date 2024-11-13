import argparse
import csv

# TODO will need to have args for output and summary log

def parse_arguments():
    parser = argparse.ArgumentParser() # parser for the file
    parser.add_argument("input", type=argparse.FileType("r"), help="file to be parsed") # required param "input" which will take the filename, holds reference to open file, ready to parse

    # optional inputs
    parser.add_argument("--title", type=str, help="Movie title") # access w/ args.title
    parser.add_argument("--released-year", type=str, help="Release year")
    parser.add_argument("--runtime", type=str, help="Duration in minutes")
    parser.add_argument(
            "--genre",
            nargs='+',  # allows multiple genres
            type=str,
            help="Main genre(s), e.g., --genre Action Drama"
        )
    parser.add_argument("--imdb_rating", type=str, help="IMDb rating on a scale of 1-10")
    parser.add_argument("--overview", type=str, help="Movie summary")
    parser.add_argument("--meta_score", type=str, help="Metascore rating")
    parser.add_argument("--director", type=str, help="Director’s name")
    parser.add_argument(
        "--stars", 
        nargs='+',
        type=str, 
        help="Top-billed actors (up to 4)")
    parser.add_argument("--votes", type=str, help="IMDb votes received")
    parser.add_argument("--gross", type=str, help="Gross revenue in USD")

    return parser.parse_args() # being used as a reference to the open file, also holds the args the user passed in for future reference
    
def collect_used_args(args):
    # stores used arg key-value pairs in dictionary for easier parsing
    used_args = {}
    for arg_name, arg_value in vars(args).items():
        if arg_value is not None: 
            used_args[arg_name] = arg_value

    return used_args

def read_csv(input_file):
    # csv dictReader auto interprets the first row as the header columns (keys) for the csv. 
    # The rows beneath are data rows (the values) for the header keys based on its position
    # use reference to open file to parse csv efficiently by changing the args namespace object to a dictionary
    reader = csv.DictReader(input_file)
    return reader
 
def filter_movies(movies, used_args):
    desired_films = []
    
    for row in movies:
        # each row is a key-value pair, access specific values by associated keys row[key]
        match = True
        matching_genres = False
        used_genres_as_arg = False
        # this loop allows me to access all arg inputs, whether they're utilized or not
        for arg_name, arg_value in used_args.items():
            
            if arg_name == "input": # required arg
                continue
            
            print(f"user arg {arg_name} has value {arg_value}, comparing to rows {row[arg_name]}")
            
            if arg_name == "genre":  # user specified genre(s)
                used_genres_as_arg = True
                genres = row[arg_name].split(',')  # split by comma
                genres = [genre.strip().lower() for genre in genres]  # clean genres and make them lowercase
                search_genres = [g.lower() for g in arg_value]  # make user inputs lowercase as well
                
                for genre in genres:
                    if genre in search_genres:
                        matching_genres = True
                        break  # No need to check further if a match is found
                else:
                    matching_genres = False
                continue

            
            if row.get(arg_name) != arg_value:
                match = False
                break
        
        # after checking through all args, specifically genres, if not one genre matches (at least the desired genre) then don't add it as it's not a match
        if used_genres_as_arg and not matching_genres :
            match = False
        # if match is true, then all user args are met in row with values, like year = 2010 or something like that
        if match: 
            desired_films.append(row)
            
    return desired_films

def print_movies(desired_films):
    for movie in desired_films:
        print(movie)
        
def main():
    args = parse_arguments()
    used_args = collect_used_args(args)
    movies = read_csv(args.input)
    desired_films = filter_movies(movies, used_args)
    print_movies(desired_films)
    
if __name__ == "__main__":
    main()
    