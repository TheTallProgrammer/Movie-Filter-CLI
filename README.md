
# Movie Data Query and Analysis CLI Tool

This CLI tool processes the IMDb Top 1000 movies dataset, allowing users to query and filter data based on multiple criteria, output results in specified formats, and generate summary statistics for filtered results.

## Features

- **Data Input**: Accepts a CSV file as input, with error handling for missing or invalid files.
- **Query Options**: Allows filtering by:
  - **Year**: Before or after a given year (`--year-before`, `--year-after`).
  - **Genre**: Movie genre(s) (`--genre`).
  - **IMDb Rating**: Above or below a specified rating (`--rating-above`, `--rating-below`).
  - **Director**: Movies by a specific director (`--director`).
  - **Actor**: Movies starring a specific actor (`--actor`).
  - **Runtime**: Movies shorter or longer than a specified duration (`--runtime-less-than`, `--runtime-more-than`).
  - **Gross**: Movies with gross revenue above or below a value (`--gross-min`, `--gross-max`).
  - **Votes**: Movies with a minimum or maximum number of votes (`--votes-min`, `--votes-max`).
- **Output**:
  - Prints filtered results to the terminal in a readable table format.
  - Maintains a sort order of IMDb rating from highest to lowest.
  - Option to save filtered data in different formats (`json`, `csv`, or plain text) with a specified file name.
- **Summary and Top 10 Lists**:
  - Generates summary logs for filtered results (`--export-log`).
  - Generates and displays Top 10 lists based on criteria such as highest-rated, most popular (by vote count), or highest-grossing movies within filtered results (`--top-10`).

**Note**: The optional features **"Genre-Based Insights"** and **"Hidden Gems Finder"** were not implemented.

## Project Structure

The project is organized into multiple modules for better maintainability and readability:

```
movie_filter_project/
├── main.py
├── argument_parser.py
├── data_reader.py
├── movie_filter.py
├── output.py
├── summary.py
└── utils.py
```

- **`main.py`**: The main script that ties all modules together.
- **`argument_parser.py`**: Handles argument parsing and validation.
- **`data_reader.py`**: Reads data from the CSV file.
- **`movie_filter.py`**: Contains logic for filtering movies based on criteria.
- **`output.py`**: Handles printing and saving the filtered movie data.
- **`summary.py`**: Generates summary logs and Top 10 lists.
- **`utils.py`**: Contains utility functions shared across modules.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/movie_filter_project.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd movie_filter_project
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

   **Note**: Ensure you have Python 3.x and `pip` installed.

## Usage

Run the program using the following command:

```bash
python main.py --input imdb_top_1000.csv [arguments]
```

Replace `[arguments]` with any of the available options.

### Available Arguments

- **Data Input**:
  - `--input`: Path to the input CSV file (required).

- **Filtering Options**:
  - `--year-before YEAR`: Include movies released before the specified year.
  - `--year-after YEAR`: Include movies released after the specified year.
  - `--genre GENRE`: Filter by genre(s). Multiple genres can be specified.
  - `--rating-above RATING`: Include movies with IMDb rating above the specified value.
  - `--rating-below RATING`: Include movies with IMDb rating below the specified value.
  - `--director DIRECTOR`: Filter movies by director's name.
  - `--actor ACTOR`: Filter movies starring a specific actor.
  - `--runtime-less-than MINUTES`: Include movies with runtime less than the specified minutes.
  - `--runtime-more-than MINUTES`: Include movies with runtime more than the specified minutes.
  - `--gross-min AMOUNT`: Include movies with gross revenue above the specified amount.
  - `--gross-max AMOUNT`: Include movies with gross revenue below the specified amount.
  - `--votes-min COUNT`: Include movies with votes above the specified number.
  - `--votes-max COUNT`: Include movies with votes below the specified number.

- **Output Options**:
  - `--output-format FORMAT`: Specify output format (`json`, `csv`, or `txt`). Default is `txt`.
  - `--output-file FILENAME`: Specify the name of the output file. Default is `filtered_movies`.
  - `--export-log LOGFILE`: Export summary log to a specified file.
  - `--top-10 CRITERIA`: Generate a Top 10 list based on criteria (`highest-rated`, `most-popular`, `highest-grossing`).

### Examples

1. **High-rated action movies after 2010, saved as JSON**:

   ```bash
   python main.py --input imdb_top_1000.csv --genre "Action" --year-after 2010 --rating-above 8 --output-format json --output-file top_action_movies.json
   ```

2. **Spielberg blockbusters with high votes, stats exported to a log file**:

   ```bash
   python main.py --input imdb_top_1000.csv --director "Steven Spielberg" --gross-min 50000000 --votes-min 200000 --output-format csv --output-file spielberg_blockbusters.csv --export-log movie_summary_log.txt
   ```

3. **Top 10 highest-rated movies starring Tom Hanks**:

   ```bash
   python main.py --input imdb_top_1000.csv --actor "Tom Hanks" --top-10 highest-rated
   ```

## Notes

- Ensure that the input CSV file (`imdb_top_1000.csv`) is correctly formatted and accessible in the project directory.
- All arguments are case-insensitive.
- **Multiple Genres**: Specify multiple genres by either repeating the `--genre` argument or by listing genres in a single argument with spaces between them:
  - Example: `--genre action --genre drama adventure`
- **Multiple Actors**: List multiple actors by separating their names with a comma:
  - Example: `--actor "brad pitt, angelina jolie"`
- The program outputs the filtered movies to the terminal by default, sorted in descending order by IMDb rating.


