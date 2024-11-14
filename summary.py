from tabulate import tabulate
import sys

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
     