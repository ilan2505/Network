CC = gcc
COMP_FLAG = -Wall 


all: measure sender

measure: measure.c 
	$(CC)  $(COMP_FLAG)   -o measure measure.c
	
sender: sender.c 
	$(CC)  $(COMP_FLAG)   -o sender sender.c	

measure.o: measure.c 
	$(CC) $(COMP_FLAG) -c $*.c

sender.o: sender.c 
	$(CC) $(COMP_FLAG) -c $*.c
	
.PHONY: clean all  

clean:
	rm -f *.a *.so *.o mains mainc
		
	


