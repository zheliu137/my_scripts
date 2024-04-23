reset
#set terminal tikz latex size 3in,2.25in
#set output "nbas_dispersion.tex"
set style data lines
set style line 1 linecolor rgb "black"
set colorsequence classic

y_ub = 450 # cm-1

cmTomEv = 0.124
cmToThz = 0.0299796138625734

unit_tfac = cmToThz

#set ylabel '$\omega$ (\si{\milli\electronvolt})'
set ylabel '$\omega$ (THz)'

set yrange [0:y_ub*unit_tfac]

set multiplot layout 1, 2
set size .75, 1
set origin 0, 0
set nokey
set rmargin 0.5

#set arrow from  0.542315134,   y_ub to  0.542315134,  -10.0 nohead
#set arrow from  0.696088210,   y_ub to  0.696088210,  -10.0 nohead
#set arrow from  0.849866802,   y_ub to  0.849866802,  -10.0 nohead
#set arrow from  1.304964062,   y_ub to  1.304964062,  -10.0 nohead     
#set arrow from  1.599884252,   y_ub to  1.599884252,  -10.0 nohead
#set arrow from  2.305162000,   y_ub to  2.305162000,  -10.0 nohead
                             
set xtics ("$\Gamma$"  0.00000,"$\Sigma$"  0.542315134,"N"  0.696088210,"$\Sigma_1$"  0.849866802,"Z"  1.304964062,"$\Gamma$"  1.599884252,"X"  2.305162)

set grid xtics

plot for [i=2:13] "disp_ns.dat" u 1:(column(i)*unit_tfac) w l lc rgb "black"

unset xtics

set size .25, 1
set origin 0.75, 0
set key bottom center samplen 3.0 font ",12"
set lmargin 0
unset rmargin
unset ylabel
set xtics ('' 0)
set format y ''
plot 'nbp.dos' using ($3+$4):($1*unit_tfac) title "Nb",\
	 'nbp.dos' using ($5+$6):($1*unit_tfac) title "P",\
	 'nbp.dos' using 2:($1*unit_tfac) title "Total"
unset multiplot
