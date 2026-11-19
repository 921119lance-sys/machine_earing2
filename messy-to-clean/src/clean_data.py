"""Clean CSV files. Only Python standard library is needed."""
import argparse
import csv
import io
from pathlib import Path

MISSING = {"", "na", "n/a", "null", "none", "nan", "?"}
ROOT = Path(__file__).resolve().parents[1]


def clean_rows(text):
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration:
        raise ValueError("CSV is empty.") from None
    header = [s.strip().lower().replace(" ", "_") for s in header]
    if not all(header) or len(set(header)) != len(header):
        raise ValueError("Column names must be nonempty and unique.")
    output, seen, count = [], set(), 0
    for row in reader:
        if len(row) != len(header):
            raise ValueError("A row has the wrong number of columns.")
        count += 1
        cleaned = tuple("" if v.strip().lower() in MISSING else v.strip() for v in row)
        if not any(cleaned) or cleaned in seen:
            continue
        seen.add(cleaned)
        output.append(cleaned)
    return header, output, count


def clean_csv(source, destination):
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError("Input and output paths must be different.")
    if not source.is_file():
        raise FileNotFoundError(f"File not found: {source}")
    header, rows, count = clean_rows(source.read_text(encoding="utf-8-sig"))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)
    return count, len(rows)


def main():
    parser = argparse.ArgumentParser(description="Clean CSV data safely.")
    parser.add_argument("input", nargs="?", help="Source CSV")
    parser.add_argument("output", nargs="?", help="Cleaned CSV")
    parser.add_argument("--demo", action="store_true", help="Try built-in sample data")
    args = parser.parse_args()

    if args.demo:
        header, rows, count = clean_rows(
            " Name , Age , City\n Alice , 20 , Taipei \n Bob,NA, Tainan\n"
            " Alice , 20 , Taipei\n , , \n"
        )
        destination = ROOT / "data" / "processed" / "demo_cleaned.csv"
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"Demo: {count} rows -> {len(rows)} rows. Saved: {destination}")
        return

    if not args.input or not args.output:
        parser.error("Give input and output paths, or use --demo.")
    try:
        count, kept = clean_csv(args.input, args.output)
    except (OSError, ValueError, UnicodeError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Input rows: {count}; cleaned rows: {kept}; removed: {count - kept}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
