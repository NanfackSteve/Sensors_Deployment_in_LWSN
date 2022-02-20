#/bin/sh

if [ -e ./parallel_version/parallel_datas_times.dat ];then
    rm ./parallel_version/parallel_datas_times.dat #suppr le fich s'il existe
fi


for i in `seq 1 10`
do
    N=$((i*1000))
    ./parallel_version/parallel_deploy.exe $N 10 1 0.4 0.5 4 $i 
    
    #recuperation du temps 
    filename=$(echo "datas_deploy_$i.dat")
    time=$(grep "time" ${filename} | cut -f 3 -d " ") 
    echo "$N $time" >> ./parallel_version/parallel_datas_times.dat
    mv datas_deploy_* ./parallel_version/parallel_datas/
done

if [ $# -gt 0 ]; then
    gnuplot parallel_script.gnu -p
fi
