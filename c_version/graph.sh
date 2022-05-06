#!/bin/bash

format_file(){
  # fonction de formatage : $1 = donnee parallele $2 = donnee sequent.
  
    paste $1 $2 > tmp.txt
    sed 's/\t/ /g' tmp.txt > formated.txt
    cut -d ' ' -f 1,2,4 formated.txt > par_vs_seq.dat

    rm tmp.txt formated.txt
}

format_file $1 $2

#Calcul du Speed Up

#Recupere le Temps sequentiel et parallel
Tp=(`cut -d ' ' -f 2 par_vs_seq.dat`)
Ts=(`cut -d ' ' -f 3 par_vs_seq.dat`)

for i in ${!Ts[@]}
do
    #calcul du speedUp de chaq lign
    speedUp=$(echo "scale=6; ${Ts[$i]}/${Tp[$i]} + 0" | bc -l)
    echo $speedUp >> speedUp.dat
done

#Ajoute ces resultat au fichier de donnees
paste par_vs_seq.dat speedUp.dat > tmp.txt
sed 's/\t/ /g' tmp.txt > par_vs_seq.dat

#Remplace les ligne qui debutent par un '.' par 0.

cat par_vs_seq.dat | awk -F " " '{gsub("^[.]","0.",$4); print $0}' > tmp.txt
cat tmp.txt > par_vs_seq.dat

rm speedUp.dat tmp.txt

gnuplot par_vs_seq_script.gnu -p
