CC = gcc # compilateur a utiliser
EXEC_S = sequential_deploy.exe # nom du programme (a generer)
EXEC_P = parallel_deploy.exe  
SCRIPT_P = parallel_n_deploy.sh #nom du prog
SCRIPT_S = sequential_n_deploy.sh 

all : $(EXEC_P) $(EXEC_S) $(SCRIPT_P) $(SCRIPT_S) #en faisant un make all cest $FILE qui s'execute
	./$(SCRIPT_S)

$(EXEC) : sequential_deploy.c
	$(CC) -o $(EXEC_S) sequential_deploy.c -lm

$(EXEC_P) : parallel_deploy.c
	$(CC) -o $(EXEC_P) parallel_deploy.c -lm -lpthread

clean :
	rm -rf *.o