# csv-analyzer-c

Command-line tool for analyzing numeric CSV files. Input a CSV, tell it which row or column you want to analyze (zero-indexed), and it returns the mean, max, and min for that row/column.

- written using C standard library
- no constraints on size of CSV files (memory-dependent)
- originally a project for 214 (systems programming) using CLI
  ... added flask web app, unlimited size, and formatting post-submission, but functionality is virtually the same

### Usage
./main.c <csv_file> <r|c> <index>

### Compile
gcc -std=c99 -Wall -O2 -o main main.c

