SCRIPT = ./graph.sh #nom du prog
TIME_S = seq_time.dat 
TIME_P = parallel_time.dat

all : $(TIME_P) $(TIME_S) $(SCRIPT)
	$(SCRIPT) $(TIME_P) $(TIME_S)

clean :
	rm -rf *.o