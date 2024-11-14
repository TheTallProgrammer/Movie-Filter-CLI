from argument_parser import parse_arguments, collect_used_args
from data_reader import read_csv
from movie_filter import filter_movies
from output import print_movies, save_filtered_data
from summary import generate_summary_log, generate_top_10_list

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
