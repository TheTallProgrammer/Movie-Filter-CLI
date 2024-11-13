import argparse
import csv

# TODO will need to have args for output and summary log

def parse_arguments():
    parser = argparse.ArgumentParser() # parser for the file
    parser.add_argument("--input", type=argparse.FileType("r"), help="file to be parsed") # required param "input" which will take the filename, holds reference to open file, ready to parse

    parser.add_argument("--year-after", type=int, help="Filter for movies released after a given year")
    parser.add_argument("--year-before", type=int, help="Filter for movies released before a given year")
    parser.add_argument(
        "--genre",
        nargs='+',  # allows multiple genres
        type=str,
        help="Filter by genre(s), e.g., --genre Action Drama"
    )
    parser.add_argument("--rating-above", type=float, help="Filter for IMDb rating above a specified value")
    parser.add_argument("--rating-below", type=float, help="Filter for IMDb rating below a specified value")
    parser.add_argument(
        "--director", 
        nargs='+', # for director first and last name as arguments
        type=str, 
        help="Filter by director’s name")
    parser.add_argument(
        "--actor",
        nargs='+',  # Collect multiple actor names
        type=str,
        help="Filter by actor's name(s), separated by commas."
)
    
    parser.add_argument("--runtime-more-than", type=int, help="Filter for movies with runtime more than a specified duration (in minutes)")
    parser.add_argument("--runtime-less-than", type=int, help="Filter for movies with runtime less than a specified duration (in minutes)")
    parser.add_argument("--gross-min", type=int, help="Filter for movies with gross revenue above a specified value in USD")
    parser.add_argument("--gross-max", type=int, help="Filter for movies with gross revenue below a specified value in USD")


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
                continue # add continue at end of arg eval in order to go to next arg in the array, no need in checking other conditions if we found the arg we're currently looking at in array
            
            # arg_name is the specified arg command user inputs ie "genre" and the arg_value is the value that follows "action"
            # the row[arg_name] pulls the value for that key from the row, so if checking genre, row[genre] will pull whatever genre(s) that row has for that movie
            
            # imdb rating
            if arg_name == "rating_above": # user wants the rating of movie to be above arg_value
                if float(row['imdb_rating']) <= float(arg_value): # checking condition that would make the movie invalid
                    match = False
                    break
                continue 
                
            if arg_name == "rating_below": # user wants rating to be less than arg_value
                if float(row["imdb_rating"]) >= float(arg_value): # checking condition that would make the movie invalid
                    match = False
                    break
                continue
            
            if arg_name == "year_after":
                if not row['released_year'].isdigit() or int(row['released_year']) <= int(arg_value):
                    match = False
                    break
                continue
            
            if arg_name =="year_before":
                if not row['released_year'].isdigit() or int(row['released_year']) >= int(arg_value):
                    match = False
                    break
                continue
            
            if arg_name == "director":
                full_name = arg_value[0].lower() + " " + arg_value[1].lower() # grab first/last name from argument
                if row['director'].lower() != full_name:
                    match = False
                    break
                continue
            
            if arg_name == "runtime_less_than":
                if int(row['runtime'].replace("min", "")) >= int(arg_value):
                    match = False
                    break
                continue
            
            if arg_name == "runtime_more_than":
                if int(row['runtime'].replace("min","")) <= int(arg_value):
                    match = False
                    break
                continue
            
            if arg_name == "gross_min":
                if not row['gross'] or int(row['gross'].replace(",","")) < int(arg_value):
                    match = False
                    break
                continue
            
            if arg_name == "gross_max":
                if not row['gross'] or int(row['gross'].replace(",","")) > int(arg_value):
                    match = False
                    break
                continue
            
            if arg_name == "genre":  # user specified genre(s)
                used_genres_as_arg = True
                genres = row[arg_name].split(',')  # split by comma if multiple genres for one movie
                genres = [genre.strip().lower() for genre in genres]  # clean genres and make them lowercase
                search_genres = [g.lower() for g in arg_value]  # make user inputs lowercase as well
                
                for genre in genres:
                    if genre in search_genres:
                        matching_genres = True
                        break  # no need to check further if a match is found
                continue

            if arg_name == "actor":
                actor_string = ' '.join(arg_value)
                arg_actor_names = [name.strip().lower() for name in actor_string.split(',')]
                csv_actor_names = []
                for i in range (1,5):
                    csv_actor_names.append(row['star_' + str(i)])
                for name in arg_actor_names:
                    if name not in csv_actor_names:
                        match = False
                        break
                continue
                    

            if row.get(arg_name) != arg_value: # if any of the args the user passed in just doesn't match values, then it voids the entire row ie genre = action, the row doesn't have action in genres, that movie is skipped 
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
    # print_movies(desired_films)
    
if __name__ == "__main__":
    main()
    