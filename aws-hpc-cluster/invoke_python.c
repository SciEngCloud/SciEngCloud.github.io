#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>
#include <string.h>

main(int argc, char **argv)
{
   int ierr, num_procs, my_id;
   char hostname[1024];
   gethostname(hostname, 1024);
   char invoke[] = "python /home/ec2-user/pi.py %d %s";
   char ninvoke[50];
   
   ierr = MPI_Init(&argc, &argv);

   /* find out MY process ID, and how many processes were started. */

   ierr = MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
   ierr = MPI_Comm_size(MPI_COMM_WORLD, &num_procs);
   sprintf(ninvoke, invoke, my_id, hostname);
   printf(" invoking: %s\n", ninvoke);
   system(ninvoke);

   //printf("Hello world! I'm process %i out of %i processes on host %s\n",
   //my_id, num_procs, hostname);
   //printf("%s\n", hostname);
   ierr = MPI_Finalize();
}
