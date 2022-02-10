CC = gcc # compilateur a utiliser
EXEC = sequential_deploy.exe # nom du programme (a generer) 
FILE = many_deployment.sh #nom du prog

all : $(EXEC) $(FILE) #en faisant un make all cest $FILE qui s'execute
	./$(FILE)

$(EXEC) : sequential_deploy.c
	$(CC) -o $(EXEC) sequential_deploy.c -lm

clean :
	rm -rf *.o