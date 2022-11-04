CC = gcc
COMP_FLAG = -Wall 


all: sniffer myping

sniffer: sniffer.o
	$(CC) $(COMP_FLAG) -o sniffer sniffer.o
myping: myping.o
	$(CC) $(COMP_FLAG) -o myping myping.o
	

sniffer.o: sniffer.c
	$(CC) $(COMP_FLAG) -c $*.c
myping.o: myping.cpp
	$(CC) $(COMP_FLAG) -c $*.cpp



	
.PHONY: clean all sniffer myping


clean:
	rm -f *.o sniffer myping
		
	


