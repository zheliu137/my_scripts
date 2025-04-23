import numpy as np

# Define the value of dosef
dosef = 0.85436  # states/Ry
RytomeV = 13605.7  # Conversion factor from Rydberg to eV

# Open the input file and process each line
processed_data = []
with open('scat_.dat', 'r') as file:
    # Skip the header line manually
    next(file)
    for line in file:
        if line.strip():  # Check if the line is not empty
            # Split the line and convert to float
            q, w, ga, g2 = map(float, line.split())
            # Calculate lambda if w is not zero
            if w != 0:
                lmbd = ga / (np.pi * w**2 * dosef / RytomeV)
            else:
                lmbd = 0.0
            # Store the processed data
            processed_data.append((q, w, ga, g2, lmbd))
        else:
            # Keep the blank lines as they are
            processed_data.append("")

# Write to the output file
with open('scat.dat', 'w') as file:
    # Write the header
    header = f"{'# q-path':>10} {'omega_q':>10} {'gamma(q)(meV)':>15} {'g(q)^2 (meV*ryd)':>20} {'lambda':>15}\n"
    file.write(header)
    
    # Define the format for each line of data to maintain column alignment
    line_format = "{:>10.4f} {:>10.4f} {:>15.4e} {:>20.4e} {:>15.4e}\n"
    
    # Write each row of data or a blank line
    for item in processed_data:
        if isinstance(item, tuple):  # Check if the item is data
            q, w, ga, g2, lmbd = item
            file.write(line_format.format(q, w, ga, g2, lmbd))
        else:
            # Write a blank line
            file.write("\n")

print("Data has been written to 'scat.dat' with aligned columns, preserving blank lines.")

