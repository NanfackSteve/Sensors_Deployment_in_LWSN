CC = gcc # compilateur a utiliser
EXEC_S = sequential_deploy.exe # nom du programme (a generer)
EXEC_P = parallel_deploy.exe  
SCRIPT_P = parallel_n_deploy.sh #nom du prog
SCRIPT_S = sequential_n_deploy.sh 
SCRIPT_SP = par_vs_seq.sh

all : $(EXEC_P) $(EXEC_S) $(SCRIPT_P) $(SCRIPT_S) #en faisant un make all cest $FILE qui s'execute
	./$(SCRIPT_S)
	./$(SCRIPT_P)
	./$(SCRIPT_SP) parallel_datas_times.dat sequential_datas_times.dat

$(EXEC) : ./sequential_version/sequential_deploy.c
	$(CC) -o ./sequential_version/$(EXEC_S) ./sequential_version/sequential_deploy.c -lm

$(EXEC_P) : ./parallel_version/parallel_deploy.c
	$(CC) -o ./parallel_version/$(EXEC_P) ./parallel_version/parallel_deploy.c -lm -lpthread

clean :
	rm -rf *.o