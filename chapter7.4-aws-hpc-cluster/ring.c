#this is the full ring test that was used to compute the message
#latency.   

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char** argv) {
  // Initialize the MPI environment
  MPI_Init(NULL, NULL);
  // Find out rank, size
  int world_rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
  int world_size;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  char hostname[1024];
  gethostname(hostname, 1024);
  time_t seconds0;
  time_t seconds1;

  
  // We are assuming at least 2 processes for this task
  if (world_size < 2) {
    fprintf(stderr, "World size must be greater than 1 for %s\n", argv[0]);
    MPI_Abort(MPI_COMM_WORLD, 1);
  }
  //printf("world size =%d\n", world_size);
  int number;
  int i;
  if (world_rank == 0) time(&seconds0);
  for(i = 0; i <= 10000; i++) {
    if (world_rank == 0) {
      // If we are rank 0, set the number to -1 and send it to process 1
      if (i == 0){
        number = -1;
        MPI_Send(&number, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
      }
      else{
        MPI_Recv(&number, 1, MPI_INT, world_size-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        number = number+1;
        MPI_Send(&number, 1, MPI_INT, world_rank+1, 0, MPI_COMM_WORLD);
        //printf("Process  received number %d from process %d on node %s\n", number-1, world_size-1, hostname);        
      }
    } else if (world_rank > 0 && world_rank < world_size) {
      MPI_Recv(&number, 1, MPI_INT, world_rank-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      number = number+1;
      if (world_rank+1 <= world_size)
          MPI_Send(&number, 1, MPI_INT, (world_rank+1)%world_size, 0, MPI_COMM_WORLD);
      //printf("Process  received number %d from process %d on node %s\n", number-1, world_rank-1, hostname);
    }  
  }
  if (world_rank == 0) time(&seconds1);
  if (world_rank == 0){
    //printf("seconds = %f\n", seconds0);
    //printf("seconds = %f\n", seconds1);
    printf("elapsted time in seconds is %f\n", difftime(seconds1,seconds0));
  }
  MPI_Finalize();
}
