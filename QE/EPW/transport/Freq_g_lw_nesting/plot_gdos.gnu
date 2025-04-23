reset
# Set the terminal (optional, depends on your output needs)
#set terminal postscript enhance
#set output 'freq_g.eps'
#set terminal pngcairo enhanced size 800,600 font "Arial,16"
#set output 'freq_g.png'

set terminal wxt font "Arial,14" size 600,400

set multiplot layout 1,2

#set lmargin at screen 0.1
set rmargin at screen 0.8

set tmargin at screen 0.9
set bmargin at screen 0.1

# Define a color palette
# set logscale cb
set palette defined ( 0 "black", 50 "yellow", 100 "red" )
set cbrange [0:15]
set cbtics 5
# set format cb "%.1tx10^{%T}"
# Manually set ticks
# set cbtics ("0" 0, "0.2" 20, "0.4" 40, "0.6" 60, "0.8" 80, "1.0x10^2" 100)

# Define total width range
total_width_start = 0.05 # Starting position of total width
total_width_end = 0.95 # Ending position of total width
total_width = total_width_end - total_width_start # Total width

# Define width ratios for plot a, plot b, and colorbar
a_width_ratio = 0.7 # Plot a occupies 40% of total width
b_width_ratio = 0.15 # Plot b occupies 40% of total width
cb_width_ratio = 0.03 # Colorbar occupies 10% of total width

# Calculate positions and widths
a_start = total_width_start
a_width = total_width * a_width_ratio

b_start = a_start + a_width
b_width = total_width * b_width_ratio

cb_start = b_start + b_width + 0.02
cb_width = total_width * cb_width_ratio

# Common height parameters
y_origin = 0.1
plot_height = 0.8

# Set position and size of plot a
set origin a_start, y_origin
set size a_width, plot_height

x1=0.0000
x2=0.9984
x3=1.2808
x4=1.5632
x5=2.4018
x6=2.9435
x7=4.2424

ymin=0.0
ymax=35.0

set yrange [ymin:ymax]

set arrow from  x1,  ymin to  x1,   ymax nohead dt '-'
set arrow from  x2,  ymin to  x2,   ymax nohead dt '-'
set arrow from  x3,  ymin to  x3,   ymax nohead dt '-'
set arrow from  x4,  ymin to  x4,   ymax nohead dt '-'
set arrow from  x5,  ymin to  x5,   ymax nohead dt '-'
set arrow from  x6,  ymin to  x6,   ymax nohead dt '-'
set arrow from  x7,  ymin to  x7,   ymax nohead dt '-'

set xtics ("{/Symbol G}"  x1, "{/Symbol S}"  x2,"N"  x3,"{/Symbol S}_1"  x4,"Z"  x5,"{/Symbol G}"  x6,"X"  x7)

unset key

set ylabel "{/Symbol w}_{q{/Symbol n}} (meV)" font "Arial,16"
set cblabel "{g}_{q{/Symbol n}} (meV)" font "Arial,16" offset 0,0

set colorbox vertical user origin cb_start, y_origin size cb_width, plot_height

set rmargin 0

# Plot figure 1
plot "scat.dat" using 1:2:(sqrt(column(4))/8) with lines lw 2.0 lc palette

# plot "scat.dat" using 1:2:(sqrt(column(4))/8) with lines lw 2.0 lc palette, \
#      '-' using 1:2 with points pt 6 ps 1 lc rgb "black" notitle
# 0.0    14.96486295
# 0.0    27.71041316
# 0.0    30.28927936
# 0.0    30.15289701
# 0.0    20.29617286
# 0.0    31.23155739
# 2.9435    14.96486295
# 2.9435    27.71041316
# 2.9435    30.28927936
# 2.9435    30.15289701
# 2.9435    20.29617286
# 2.9435    31.23155739
# e
# plot "scat.dat" using 1:2:(sqrt(column(4))) with lines lw 2.0 lc palette

# Set position and size of plot b
set origin b_start, 0.1 # Origin position of plot b
set size b_width, 0.8 # Size of plot b

# Plot figure 2
set origin b_start, y_origin
set size b_width, plot_height
unset xlabel
unset xtics
set format y ""
set ytics 5
unset ylabel
set key right bottom samplen 0.8 font "Arial,12"

set lmargin 0

set xrange [0:0.3]

plot 'dos.dat' u 2:($1*0.124) w l lw 2 lc rgb "black" title 'Total', \
     'dos.dat' u 3:($1*0.124) w l lw 2 lc rgb "blue" title 'Ta', \
     'dos.dat' u 5:($1*0.124) w l lw 2 lc rgb "red" title 'As'
	 
unset multiplot
#set output
