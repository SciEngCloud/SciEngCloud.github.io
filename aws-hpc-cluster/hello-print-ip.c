#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>

main(int argc, char **argv)
{
   int ierr, num_procs, my_id;
   char hostname[1024];
   gethostname(hostname, 1024);
   ierr = MPI_Init(&argc, &argv);
   ierr = MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
   ierr = MPI_Comm_size(MPI_COMM_WORLD, &num_procs);
   printf("%s\n", hostname);
   ierr = MPI_Finalize();
}
