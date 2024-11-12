import argparse
import csv

parser = argparse.ArgumentParser() # parser for the file
parser.add_argument("input", type=argparse.FileType("r"), help="file to be parsed") # required param "input" which will take the filename, holds reference to open file, ready to parse

# optional inputs
parser.add_argument("--title", type=str, help="Movie title") # access w/ args.title
parser.add_argument("--year", type=str, help="Release year")
parser.add_argument("--runtime", type=str, help="Duration in minutes")
parser.add_argument("--genre", type=str, help="Main genre(s), e.g., 'Drama, Comedy'")
parser.add_argument("--imdb_rating", type=str, help="IMDb rating on a scale of 1-10")
parser.add_argument("--overview", type=str, help="Movie summary")
parser.add_argument("--meta_score", type=str, help="Metascore rating")
parser.add_argument("--director", type=str, help="Director’s name")
parser.add_argument("--stars", type=str, help="Top-billed actors (up to 4)")
parser.add_argument("--votes", type=str, help="IMDb votes received")
parser.add_argument("--gross", type=str, help="Gross revenue in USD")

# TODO will need to have args for output and summary log

args = parser.parse_args() # being used as a reference to the open file, also holds the args the user passed in for future reference

# stores used arg key-value pairs in dictionary for easier parsing
used_args = {}
for arg_name, arg_value in vars(args).items():
    if arg_value is not None: 
        used_args[arg_name] = arg_value

try:
    desired_films = []
    
    # csv dictReader auto interprets the first row as the header columns (keys) for the csv. 
    # The rows beneath are data rows (the values) for the header keys based on its position
    reader = csv.DictReader(args.input) # use reference to open file to parse csv efficiently by changing the args namespace object to a dictionary
    
    for row in reader:
        # each row is a key-value pair, access specific values by associated keys row[key]
        
        match = True
        # this loop allows me to access all arg inputs, whether they're utilized or not
        for arg_name, arg_value in used_args.items():
            
            if arg_name == "input": # required arg
                continue
            
            # this condition fails because it requires everything to have a value that the user wants or it's false
            # need to make a condition that checks the row has all required args, the rest don't matter what value it is, not the other condition, which requires all args in the current row to have only the users args, which is never the case unless the user inputs all optional args in the command line 
            if row.get(arg_name) != arg_value:
                match = False
                break
            
            # I need a way to essentially compare values of the args in the row to the values of args that the user wants the movies to have, if the args don't match that's fine, it just needs to have at least the args that do. So maybe the inverse is the best way? Don't necessarily compare for matching values, but maybe check to see what values the row doesn't match with, subtract that from all args, and then if the remaining args match the users passed in args, add that row of data, sort of like 1-P(x) instead of p(specific condition)

        if match:
            desired_films.append(row)

finally:
    args.input.close() # close the open file rerference 
    
for movie in desired_films:
    print(movie)