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
            print(f"argname: {arg_name}, argvalue: {arg_value}")
            
            if arg_name == "input": # required arg
                continue
            
            # an issue with this is that the genre can have multiple genres, need to parse through them to see if one matches the desired arg from user
            if arg_name == "genre" and row.get(arg_name) == arg_value: # meaning the user inputted genre and this specific row has desired arg
                for genre in arg_value:
                    # if()
                    pass
            
            if row.get(arg_name) != arg_value:
                match = False
                break
            
        if match:
            desired_films.append(row)

finally:
    args.input.close() # close the open file rerference 
    
# for movie in desired_films:
#     print(movie)