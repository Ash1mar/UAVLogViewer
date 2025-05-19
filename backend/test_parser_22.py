# backend/test_parse.py

from parser.mav_parser import parse_bin


def main():
    path = "data/sample1_after PropBalance.bin"
    df = parse_bin(path)

    print("Parsed rows:", len(df))
    print("Columns:", df.columns.tolist())
    print("Head:")
    print(df.head(5))


if __name__ == "__main__":
    main()
