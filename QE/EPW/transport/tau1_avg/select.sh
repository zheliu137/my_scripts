
# This script is for using 1/10 of the data points to speed up plotting and clean up the figure.
SR=$1

sort $SR > out
sed -n '1~10p' out > out2

mv out2 p_$1

rm -f out