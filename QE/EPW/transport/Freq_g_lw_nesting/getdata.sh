#!/bin/bash
echo "The default number of atoms is 4, use 'sh getdata.sh natom' to change it"

natom=$1

if [ -z "$natom" ]; then
  natom=4
fi

grep gamma___ epw.out > SE_tmp.dat
grep gamma_g2 epw.out > g2_tmp.dat

grep 'Nest_func' epw.out | cut -c 26-31 > qpath_.dat
grep 'Nest_func' epw.out | cut -c 80-94 > nesting_.dat

# Nesting function
paste qpath_.dat nesting_.dat > nesting.dat
rm -rf nesting_.dat

rm -rf SE_.dat
rm -rf g2_.dat
rm -rf freq.dat
rm -rf qpath.dat

for i in $(seq 1 $((natom * 3)))
do
cat qpath_.dat >> qpath.dat
echo " " >> qpath.dat
sed -n "$i~12p" SE_tmp.dat | cut -c 50-65 >> SE_.dat
echo " " >> SE_.dat
sed -n "$i~12p" SE_tmp.dat | cut -c 78-90 >> freq.dat
echo " " >> freq.dat
sed -n "$i~12p" g2_tmp.dat | cut -c 50-65 >> g2_.dat
echo " " >> g2_.dat
done

# Write into file
echo "#     q-path      omega_q           \gamma(q)(meV)         g(q)^2 (meV^2)" > freq_SEg2.dat
#paste freq.dat SE_.dat g2_.dat >> freq_SEg2.dat
paste qpath.dat freq.dat SE_.dat g2_.dat >> freq_SEg2.dat

mv freq_SEg2.dat scat.dat

rm -rf SE_.dat
rm -rf g2_.dat
rm -rf freq.dat
rm -rf qpath.dat
#rm -rf nesting.dat
rm -rf qpath_.dat
rm -rf *tmp*
