import argparse
import sys

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

