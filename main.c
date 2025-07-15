#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <limits.h>

#define LINE_BUF_SIZE 2048
#define DELIM ","  // Change to other delimiters if you wish

// Read a line from file, return NULL on EOF/error
char *read_line(FILE *fp) {
    static char buf[LINE_BUF_SIZE];
    if (fgets(buf, sizeof(buf), fp) == NULL) return NULL;
    size_t len = strlen(buf);
    if (len && buf[len-1] == '\n') buf[len-1] = '\0';
    return buf;
}

// Parse a line into a uint32_t array. Returns number of columns.
// 'cols_out' gets a newly malloc'd array of the values.
// Returns -1 on error.
int parse_line(const char *line, uint32_t **cols_out) {
    // Copy so we can use strtok
    char *tmp = strdup(line);
    int cap = 16, n = 0;
    uint32_t *vals = malloc(cap * sizeof(uint32_t));
    char *tok = strtok(tmp, DELIM);
    while (tok) {
        char *end;
        errno = 0;
        unsigned long v = strtoul(tok, &end, 10);
        if (errno || *end || v > UINT32_MAX) {
            free(tmp); free(vals);
            return -1;  // parse error
        }
        if (n == cap) {
            cap *= 2;
            vals = realloc(vals, cap * sizeof(uint32_t));
        }
        vals[n++] = (uint32_t)v;
        tok = strtok(NULL, DELIM);
    }
    free(tmp);
    *cols_out = vals;
    return n;
}

// Load CSV file: returns 2D array, and sets rows/cols_out (array of column counts per row).
uint32_t **load_csv(const char *filename, int *rows_out, int **cols_per_row_out) {
    FILE *fp = fopen(filename, "r");
    if (!fp) return NULL;

    int cap = 32, rows = 0;
    uint32_t **data = malloc(cap * sizeof(uint32_t *));
    int *cols_per_row = malloc(cap * sizeof(int));

    char *line;
    while ((line = read_line(fp))) {
        uint32_t *row;
        int ncol = parse_line(line, &row);
        if (ncol < 0) {
            // Bad value in CSV
            for (int i=0; i<rows; ++i) free(data[i]);
            free(data); free(cols_per_row);
            fclose(fp);
            return NULL;
        }
        if (rows == cap) {
            cap *= 2;
            data = realloc(data, cap * sizeof(uint32_t *));
            cols_per_row = realloc(cols_per_row, cap * sizeof(int));
        }
        data[rows] = row;
        cols_per_row[rows] = ncol;
        rows++;
    }
    fclose(fp);
    *rows_out = rows;
    *cols_per_row_out = cols_per_row;
    return data;
}

void free_csv(uint32_t **data, int rows, int *cols_per_row) {
    for (int i=0; i<rows; ++i) free(data[i]);
    free(data);
    free(cols_per_row);
}

void compute_stats(const uint32_t *arr, int n, double *mean, uint32_t *max, uint32_t *min) {
    if (n <= 0) { *mean = 0.0; *max = 0; *min = 0; return; }
    uint64_t sum = 0;
    *max = *min = arr[0];
    for (int i=0; i<n; ++i) {
        if (arr[i] > *max) *max = arr[i];
        if (arr[i] < *min) *min = arr[i];
        sum += arr[i];
    }
    *mean = (double)sum / n;
}

void print_usage(const char *prog) {
    printf("Usage: %s <file_path> <r|c> <index>\n", prog);
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        print_usage(argv[0]);
        return -1;
    }

    const char *file_path = argv[1];
    char type = argv[2][0];
    int index = atoi(argv[3]);
    if (type != 'r' && type != 'c') {
        printf("char entered must be 'r' for row or 'c' for column\n");
        return -1;
    }
    if (index < 0) {
        printf("index must be non-negative\n");
        return -1;
    }

    int rows, *cols_per_row;
    uint32_t **data = load_csv(file_path, &rows, &cols_per_row);
    if (!data) {
        printf("Error opening file or parsing CSV data\n");
        return -1;
    }

    if (type == 'r') {
        if (index >= rows) {
            printf("error in input format at line %d\n", index+1);
            free_csv(data, rows, cols_per_row);
            return -1;
        }
        int ncols = cols_per_row[index];
        double mean; uint32_t max, min;
        compute_stats(data[index], ncols, &mean, &max, &min);
        printf("%s row %.2f %u %u\n", file_path, mean, max, min);
    } else { // type == 'c'
        // check that all rows have enough columns
        for (int i=0; i<rows; ++i) {
            if (index >= cols_per_row[i]) {
                printf("error in input format at line %d\n", 1);
                free_csv(data, rows, cols_per_row);
                return -1;
            }
        }
        uint32_t *colvals = malloc(rows * sizeof(uint32_t));
        for (int i=0; i<rows; ++i) {
            colvals[i] = data[i][index];
        }
        double mean; uint32_t max, min;
        compute_stats(colvals, rows, &mean, &max, &min);
        printf("%s column %.2f %u %u\n", file_path, mean, max, min);
        free(colvals);
    }

    free_csv(data, rows, cols_per_row);
    return 0;
}
