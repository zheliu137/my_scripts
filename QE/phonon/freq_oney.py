import sys

if len(sys.argv) != 3:
    print("Usage: python script.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Read the original data
with open(input_file, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# Parse the data into rows of floats
data = [list(map(float, line.split())) for line in lines]

# Transpose the data: separate x and w1...wn
transposed_blocks = list(zip(*data))  # First column is x, rest are w1, w2, ...

# Write the reformatted blocks
with open(output_file, 'w') as f:
    for j in range(1, len(transposed_blocks)):  # Skip x column (index 0)
        for i in range(len(transposed_blocks[0])):
            x = transposed_blocks[0][i]
            wj = transposed_blocks[j][i]
            f.write(f"{x:.6f} {wj:.6f}\n")
        f.write("\n")  # Blank line
