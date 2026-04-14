"""
CLI Entrypoint — Top Scorers

"""
import sys
import os
from app.csv_parser import parse_csv
from app.database import init_db, insert_scores, get_top_scorers

DEFAULT_CSV = "TestData.csv"


def load_csv(filepath: str) -> str:
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def print_top_scorers():

    """
    Fetches results from the DB and prints them to STDOUT.
    Format: Name1 Name2
            Score: X
    """
    scorers, max_score = get_top_scorers()

    if not scorers:
        print("No scores found.") #Error Handling for no scores in DB
        return

    for scorer in scorers:
        print(scorer["full_name"])
# Print the score on the following line
    print(f"\nScore: {max_score}")



"""Orchestrates the file reading, parsing, and database insertion."""

def run_cli(csv_path: str):
    print(f"Reading from: {csv_path}\n")
    raw = load_csv(csv_path)
    records = parse_csv(raw)

    if not records:
        print("No valid records found in CSV.", file=sys.stderr)
        sys.exit(1)

# Prepare database and refresh with new data
    init_db()
    insert_scores(records)

    print("Top Scorer(s):")
    print("-" * 20)
    # Output results to STDOUT as requested
    print_top_scorers()


"""Launches the Flask development server."""
def run_api():
    from app.api import app
    print("Starting API server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--serve" in args:
        run_api()
    else:
        # Use provided path or fallback to the default TestData.csv
        csv_path = args[0] if args else DEFAULT_CSV
        run_cli(csv_path)