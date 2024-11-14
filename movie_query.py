import argparse
import csv
from tabulate import tabulate
import json
import sys

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
    parser.add_argument("--votes-min", type=int, help="Filter for minimum number of votes movie recieved")
    parser.add_argument("--votes-max", type=int, help="Filter for maximum number of votes movie recieved")
    parser.add_argument("--rating-above", type=float, help="Filter for IMDb rating above a specified value")
    parser.add_argument("--rating-below", type=float, help="Filter for IMDb rating below a specified value")
    parser.add_argument(
        "--director", 
        nargs='+', # for director first and last name as arguments
        type=str, 
        help="Filter by director’s name")
    parser.add_argument(
        "--actor",
        nargs='+',  # collect multiple actor names
        type=str,
        help="Filter by actor's name(s), separated by commas."
)
    
    parser.add_argument("--runtime-more-than", type=int, help="Filter for movies with runtime more than a specified duration (in minutes)")
    parser.add_argument("--runtime-less-than", type=int, help="Filter for movies with runtime less than a specified duration (in minutes)")
    parser.add_argument("--gross-min", type=int, help="Filter for movies with gross revenue above a specified value in USD")
    parser.add_argument("--gross-max", type=int, help="Filter for movies with gross revenue below a specified value in USD")
    parser.add_argument("--output-format", type=str, help="The acceptable formats are json, csv or plain-text")
    parser.add_argument("--output-file", type=str, help="Enter the name of the file you want to save output to")
    parser.add_argument("--export-log", type=str, help="Enter the title and filetype of the log, ie 'movie_summary_log.txt', ensure '_' for multiple words")
    parser.add_argument("--top-10", type=str, help="Generate Top 10 list based on criteria")

    validate_arguments(parser.parse_args())
    
    return parser.parse_args() # being used as a reference to the open file, also holds the args the user passed in for future reference

def validate_arguments(args):
    # validate year ranges
    current_year = 2024  
    if args.year_after and (args.year_after < 1900 or args.year_after > current_year):
        parser_error(f"--year-after must be between 1900 and {current_year}.")
    
    if args.year_before and (args.year_before < 1900 or args.year_before > current_year):
        parser_error(f"--year-before must be between 1900 and {current_year}.")
    
    if args.year_after and args.year_before:
        if args.year_after >= args.year_before:
            parser_error("--year-after must be less than --year-before.")
    
    # validate rating ranges
    if args.rating_above is not None and not (0.0 <= args.rating_above <= 10.0):
        parser_error("--rating-above must be between 0.0 and 10.0.")
    
    if args.rating_below is not None and not (0.0 <= args.rating_below <= 10.0):
        parser_error("--rating-below must be between 0.0 and 10.0.")
    
    if args.rating_above and args.rating_below:
        if args.rating_above >= args.rating_below:
            parser_error("--rating-above must be less than --rating-below.")
    
    # validate votes
    if args.votes_min is not None and args.votes_min < 0:
        parser_error("--votes-min must be a non-negative integer.")
    
    if args.votes_max is not None and args.votes_max < 0:
        parser_error("--votes-max must be a non-negative integer.")
    
    if args.votes_min and args.votes_max:
        if args.votes_min > args.votes_max:
            parser_error("--votes-min must be less than or equal to --votes-max.")
    
    # validate runtime
    if args.runtime_more_than is not None and args.runtime_more_than <= 0:
        parser_error("--runtime-more-than must be a positive integer.")
    
    if args.runtime_less_than is not None and args.runtime_less_than <= 0:
        parser_error("--runtime-less-than must be a positive integer.")
    
    if args.runtime_more_than and args.runtime_less_than:
        if args.runtime_more_than >= args.runtime_less_than:
            parser_error("--runtime-more-than must be less than --runtime-less-than.")
    
    # validate gross
    if args.gross_min is not None and args.gross_min < 0:
        parser_error("--gross-min must be a non-negative integer.")
    
    if args.gross_max is not None and args.gross_max < 0:
        parser_error("--gross-max must be a non-negative integer.")
    
    if args.gross_min and args.gross_max:
        if args.gross_min > args.gross_max:
            parser_error("--gross-min must be less than or equal to --gross-max.")
    
    # validate director name
    if args.director and len(args.director) < 2:
        parser_error("--director requires both first and last name, e.g., '--director First Last', seperate other names with comma, no "" allowed.")
    
    # validate actor names (assuming at least one actor is provided)
    if args.actor:
        for actor in args.actor:
            if not actor.strip():
                parser_error("Actor names cannot be empty.")
                
def parser_error(message):
    print(f"Argument Error: {message}", file=sys.stderr)
    sys.exit(1)
    
def collect_used_args(args):
    # store only relevant filtering args, excluding output-related arguments
    used_args = {}
    for arg_name, arg_value in vars(args).items():
        if arg_value is not None and arg_name not in {"top_10", "output_file", "output_format", "export_log"}:
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
                
            if arg_name == "votes_min":
                if int(row['no_of_votes']) < int(arg_value):
                    match = False
                    break
                continue
            
            if arg_name == "votes_max":
                if int(row['no_of_votes']) > int(arg_value):
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
                    csv_actor_names.append(row['star_' + str(i)].lower())
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
            
def generate_summary_log(desired_films, log_file):
    if not desired_films:
        log_data = "No movies matched the specified filters."
    else:
        # calculate statistics for the summary
        total_movies = len(desired_films)
        avg_rating = sum(float(movie["imdb_rating"]) for movie in desired_films) / total_movies
        min_rating = min(float(movie["imdb_rating"]) for movie in desired_films)
        max_rating = max(float(movie["imdb_rating"]) for movie in desired_films)
        avg_runtime = sum(int(movie["runtime"].replace("min", "").strip()) for movie in desired_films) / total_movies
        
        log_data = (
            f"Summary of Filtered Movies:\n"
            f"Total Movies: {total_movies}\n"
            f"Average IMDb Rating: {avg_rating:.2f}\n"
            f"Minimum IMDb Rating: {min_rating}\n"
            f"Maximum IMDb Rating: {max_rating}\n"
            f"Average Runtime: {avg_runtime:.2f} minutes\n"
        )
    
    # write summary log to file
    with open(log_file, mode="w", encoding="utf-8") as file:
        file.write(log_data)
    print(f"Summary log saved to {log_file}")
    
def generate_top_10_list(desired_films, criteria):
    if not desired_films:
        print(f"No movies found to generate a top 10 list for '{criteria}'.")
        return
    sorted_movies = []
    # sorting based on the criteria and selecting the top 10
    if criteria == "highest-rated":
        sorted_movies = sorted(desired_films, key=lambda x: float(x.get("imdb_rating", 0)), reverse=True)
    elif criteria == "most-popular":
        sorted_movies = sorted(desired_films, key=lambda x: int(x.get("no_of_votes", 0)), reverse=True)
    elif criteria == "highest-grossing":
        # Handle missing gross values, treating missing values as 0 for sorting
        sorted_movies = sorted(desired_films, key=lambda x: int(x.get("gross", "0").replace(",", "")), reverse=True)
    else:
        print("\nCriteria not accepted")
        sys.exit(1)

    # slice top 10 after sorting
    top_10 = sorted_movies[:10]

    # display the top 10 list
    headers = ["Title", "Year", "Rating", "Votes", "Gross"]
    table = [
        [
            movie.get("series_title", "N/A"),
            movie.get("released_year", "N/A"),
            movie.get("imdb_rating", "N/A"),
            movie.get("no_of_votes", "N/A"),
            movie.get("gross", "N/A")
        ]
        for movie in top_10
    ]
    print(f"\nTop 10 {criteria.replace('-', ' ')} Movies:")
    print(tabulate(table, headers=headers, tablefmt="plain"))
            
def main():
    args = parse_arguments()
    used_args = collect_used_args(args)
    movies = read_csv(args.input)
    desired_films = filter_movies(movies, used_args)
    headers = print_movies(desired_films)
    save_filtered_data(
        desired_films,
        headers,
        file_name=args.output_file,
        file_type=args.output_format
    )
    
    if args.export_log:
        generate_summary_log(desired_films, args.export_log)
    
    if args.top_10:
        generate_top_10_list(desired_films, args.top_10)
    
if __name__ == "__main__":
    main()
    