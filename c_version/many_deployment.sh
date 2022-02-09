#/bin/sh

if [ -e sequential_datas_times.dat ];then
    rm sequential_datas_times.dat #suppr le fich s'il existe
fi


for i in `seq 1 10`
do
    N=$((i*1000))
    ./sequential_deploy.exe $N 10 1 0.4 0.5 $i 
    
    #recuperation du temps 
    filename=$(echo "datas_deploy_$i.dat")
    time=$(grep "time" ${filename} | cut -f 3 -d " ") 
    echo -e "$N $time" >> sequential_datas_times.dat
done

gnuplot script.gnu -p
