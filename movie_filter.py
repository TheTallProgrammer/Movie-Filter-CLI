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
