import numpy as np
import sys

# Check if the correct number of arguments was provided
if len(sys.argv) != 3:
    print("Usage: python script.py file1.dat file2.dat")
    sys.exit(1)

filename1, filename2 = sys.argv[1], sys.argv[2]

# Process the data
data1, data2 = [], []
with open(filename1, 'r') as file1, open(filename2, 'r') as file2:
    # Skip headers or initial non-data lines if necessary
    next(file1)
    next(file2)

    for line1, line2 in zip(file1, file2):
        if line1.strip() and line2.strip():
            fields1 = list(map(float, line1.split()))
            fields2 = list(map(float, line2.split()))

            # Compute differences for the 3rd and 5th columns
            diff3 = fields1[2] - fields2[2]
            diff5 = fields1[4] - fields2[4]

            # Append the results along with the 1st and 2nd columns of file1
            data1.append((fields1[0], fields1[1], diff3, diff5))
        else:
            # Append an empty string to preserve the format
            data1.append("")

# Output the results
with open('scat_diff.dat', 'w') as output:
    header = f"{'# q-path':>20} {'omega(meV)':>20} {'lw_diff(meV)':>20} {'lambda_diff':>20}\n"
    output.write(header)
    line_format = "{:>20.6f} {:>20.6f} {:>20.5e} {:>20.5e}\n"

    for item in data1:
        if isinstance(item, tuple):
            output.write(line_format.format(*item))
        else:
            output.write("\n")

print("Differences have been calculated and written to 'scat_diff.dat' with preserved blank lines.")

