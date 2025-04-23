# Plot scattering rates and the average at each energy tics.
reset

set terminal qt  font "Arial,16"

set yrange [0.02:45]
set xrange [-0.1:0.1]
#set key autotitle columnhead
set key left top

set ytics 20

set xlabel "E-E_f(eV)"
set ylabel "1/{/Symbol t}(1/ps)"
set key samplen 3
#plot for [i=5:11:2] 'inv_tau_50.dat' u ($3*13.605-17.0633):(column(i)*20670.6944033) #ps 0.1

SR0="p_SR0.dat"
SR25="p_SR25.dat"
SR_25="p_SR-25.dat"
avg="avg.dat"

#plot 'SR_25meV.dat' u ($1*13.605-17.0633):(column(7)*20670.6944033) title "25meV"  ps 0.5 lc rgb '#CCFF0000' ,\
#     'SR_-25meV.dat' u ($1*13.605-17.0633):(column(7)*20670.6944033) title "-25meV" ps 0.5 lc rgb '#CC0000FF', \
#	 'inv_tau_0meV.fmt' u ($1*13.605-17.0633):(column(7)*20670.6944033) title "0meV" ps 0.5 lc rgb '#CC000000'
	 
plot SR0 u ($1*13.605-17.0633):(column(7)*20670.6944033) title " 0meV" ps 1.0 lc rgb '#AA000000'	, \
     SR_25 u ($1*13.605-17.0383):(column(7)*20670.6944033) title "-25meV" ps 1.0 lc rgb '#AA0000FF', \
     SR25 u ($1*13.605-17.0883):(column(7)*20670.6944033) title "25meV" ps 1.0 lc rgb '#AAFF0000'


replot avg u 1:(column(2)*20670.6944033) w l title " 0meV-avg"  lw  2.7 lc rgb '#000000'
replot avg u 1:(column(3)*20670.6944033) w l title "-25meV-avg" lw 2.7 lc rgb '#0000FF'
replot avg u 1:(column(4)*20670.6944033) w l title " 25meV-avg" lw 2.7 lc rgb '#FF0000'

#plot 'inv_tau_0meV.fmt' u ($1*13.605-17.0633):(column(7)*20670.6944033) title "0meV" ps 0.5 lc rgb '#CC000000'	 
