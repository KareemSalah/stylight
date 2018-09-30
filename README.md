### Problem 2 Solution

## Solution Algorith Walkthrouh:
  Here's how I approached this problem:
  1. I noticed that the table doesn't have any unique way to work with any <td>
  2. I loop on the table rows, and add a class `row-x` where x is the row's index (0 top row, and 42 bottom row)
  3. I loop on each table data piece inside the row and adds a class `clm-y`
  4. During that loop in step 3. I extract the field's data and create a 2d matrix in-memory to hold table data
  5. I attach event handlers (click event) to each header name
  6. When a click is triggered on a header, the sort starts
  7. I implemented a merge sort (both in-place and using scratch array)
  8. I faced a problem after I tested, run-time is more than 1000ms
  9. I did some analysis using Chrome's dev tools performance tab and found out that rendering time is 7x times the script time (700+ms)
  10. Figured out that many dom access is causing horrible rendering time
  11. Started optimizing and got rid of most of them (using datastructures in steps 4.)
  12. Voila :)


## Complexsity Analysis:
  1. Theoretically I'm doing an in-place merge sort with a rotating technique, on worst cases this can take up to O(N^2) due to rotations
  2. However using the scratch array that I also implemented, worst case scenario is O(NlogN) but with a O(N) auxiliary space
  3. String comparisons is done in O(M) assuming all strings are of length M
  4. Assuming that we have R rows, then worst case scenario is to compare all R strings in M time for NlogN time, yielding O(MNlogN)
  5. Best case is to have all the column of numbers, thus compare in O(1), yielding O(NlogN)
  6. Using the in-place merging algorithm, worst case can reach (M(N^2)logN)

## Notes:
  1. While comparing two values (either strings or numbers) and there's a tie, the breaker is the index of the first occuring value in the original table
  1. This is keeping the sort predictable