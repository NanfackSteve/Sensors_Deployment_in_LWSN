CC = gcc # compilateur a utiliser
EXEC = sequential_deploy.exe # nom du programme (a generer)
FILE = sensors_deploy.c

all : $(EXEC) $(FILE) 
	./$(EXEC) 30 10 1 0.4 0.5

$(EXEC) : $(FILE)
	$(CC) -o $(EXEC) $(FILE) -lm -lpthread

clean :
	rm -rf *.o