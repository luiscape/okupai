public class GraphonEstimator{
  public Graph g;
  public Double[][] w_est;
  public int[] clusters;
  public int n;
  public int nclusters;
  
  public GraphonEstimator(Graph g){
    this.g = g;
    this.n = g.N;
    this.clusters=new int[this.n];
    this.w_est=new Double[this.n][this.n];
    
    for (int i=0;i<this.n;i++){
     clusters[i]=-1; 
    }
  }
  
  public GraphonEstimator(int[][] M){
    
    this.n=M[0].length;
    int k = M.length;
    this.g= new Graph(this.n,k+1);
    this.clusters=new int[this.n];
    for (int i=0;i<this.n;i++){
      clusters[i]=-1; 
    }
    
    for (int i=0;i<this.n;i++){
      clusters[i]=-1; 
    }
    

   
   
    for (int obs=0;obs<k;obs++){
      int[] vet = M[obs];
      for(int i=0;i<this.n;i++){
        for(int j=0;j<i;j++){
         if(vet[i]>=0 && vet[j]>=0){
           if(vet[i]==1&&vet[j]==1)
            this.g.add_obs(i,j,1);  
           else
             this.g.add_obs(i,j,0);
          
          }
          
        } 
      }
         
    }
    
  }
  
  
  
  
  public void get_clusters(Double delta){
    int n = this.n;
    Double d=delta*delta;
    int nclusters=0;
    
    int[] cluster_center = new int[n];
    int[] sequence = new int[n];
    for (int i=0;i<n;i++){
      sequence[i]=i;
      cluster_center[i] = -1;
    }
    
  
    cluster_center[0] = sequence[0];
    nclusters++;
    this.clusters[cluster_center[0]] = 0;
    
    
    for (int i=1;i<n;i++){
      Double min_dist=delta+1;
      for (int k=0;k<nclusters;k++){
       
       Double dist=g.dist(i,cluster_center[k]);
       
       if (dist<min_dist){
         this.clusters[i]=k;
         min_dist=dist;
       }
       
      }
      if(min_dist>d){
       cluster_center[nclusters]=i;
       this.clusters[i]=nclusters;
       nclusters++;
      }
    }
    this.nclusters=nclusters;
    
  }
  
  
  
}//end of class