CVFLAG =  `pkg-config --cflags opencv` `pkg-config --libs opencv`
FLAGS    = -L /lib64 -g -O0
LIBS     = -l pthread

all:test.o
	g++ -o senddata test.o $(CVFLAG) $(FLAGS) $(LIBS)

test.o:test.cpp
	g++ -Wall -c test.cpp $(CVFLAG) $(FLAGS) $(LIBS)
test.o:clientClass.h capture.h

clean:
	rm -f senddata test.o
