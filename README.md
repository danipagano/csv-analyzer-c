# csv-analyzer-c

A straightforward command-line tool for analyzing numeric CSV files. You give it a CSV, tell it which row or column you want to analyze (zero-indexed), and it returns the mean, max, and min for that row/column.

- written using C standard library
- no constraints on size of CSV files (memory-dependent)

### Usage
./main.c <csv_file> <r|c> <index>

### Compile
gcc -std=c99 -Wall -O2 -o main main.c
