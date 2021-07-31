LIBRARY_DIR=$(ITENSOR)
include $(LIBRARY_DIR)/this_dir.mk
include $(LIBRARY_DIR)/options.mk
INC+=-I${ITENSOR}
INC+=-I${TENSORFT}/include/
INC+=-I${TENSORTIMEEV}/include/
INC+=-I${TENSOR}/TDVP/
INC+=-I${TENSOR}/parallel_tdvp_lbo
INC+=-I${TENSORTOOLS}/include
INC+=-I$(PWD)/include
INC+=-I${EIGEN}
INC+=-I${EINC}


LIBSLINK+=-L${MANYBODY}/libs
LIBSLINK+=-L${ELIBS}
LIBSPATH=-L$(ITENSOR)/lib
LIBSPATH+=$(LIBSLINK)



LIBS=-litensor -lboost_program_options
LIBSG=-litensor-g -lboost_program_options

#########################

CCFLAGS+=-I. $(ITENSOR_INCLUDEFLAGS) $(OPTIMIZATIONS) -Wno-unused-variable -std=c++17 -O2 -std=gnu++1z
CCGFLAGS+=-I. $(ITENSOR_INCLUDEFLAGS) $(DEBUGFLAGS) 

LIBFLAGS=-L$(ITENSOR_LIBDIR) $(ITENSOR_LIBFLAGS) -lboost_program_options -lboost_filesystem 
LIBGFLAGS=-L$(ITENSOR_LIBDIR) $(ITENSOR_LIBGFLAGS) -lboost_program_options -lboost_filesystem 
MPICOM=mpicxx -m64 -std=c++17 -fconcepts -fPIC



CPPFLAGS_EXTRA += -O2 -std=c++17
#MPILINK= -lboost_serialization -lboost_mpi  -I$MPI_INCLUDE -L$MPI_LIB 

MPICOM=mpicxx -m64 -std=c++17 -fconcepts -fPIC
DB=-g
CXX=g++
ND=-DNDEBUG

#-fopenmp -DOMPPAR

#
#BINS=

OBJECTS=holGS2d
all: $(OBJECTS)
#######################################

boxes: boxes_dir/boxes.cpp $(ITENSOR_LIBS) 
	$(CCCOM) $< -o bin/$@ $(CCFLAGS) $(INC) $(LIBFLAGS) 

clean:
	rm bin/*

