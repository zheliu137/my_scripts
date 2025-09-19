rm -rf Distribution_nk.fmt 
ln -s Distribution_nk.fmt.$1 Distribution_nk.fmt 
python vel_contr.py $1
mv sigma_v_distribution.dat sigma_v_distribution.dat.$1
