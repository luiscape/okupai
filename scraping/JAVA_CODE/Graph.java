public class Graph{
  public Edge[][] edge;
  public int N;
  public int max_obs;
  
  public Graph(int N, int max_obs){
    
    edge = new Edge[N][N];
    this.N=N;
    this.max_obs=max_obs;
    for (int i = 0;i < N;i++){
      for(int j=0;j<N;j++){
       edge[i][j]=new Edge(i,j,max_obs); 
      }
    }
  }
  
  public void add_obs(int i, int j, int value){
 //    System.out.println("Adding edge in graph "+i+"-"+j+" ___ "+value);
 //    System.out.println(this.edge[i][j]);
   this.edge[i][j].add_obs(value); 
   if(i!=j)
     this.edge[j][i].add_obs(value); 
  }
  
  public Double dist(int i, int j){
    int n=0;
    Double d=0.0;
    for (int k=0;k<this.N && k!=i && k!=j;k++){
     
      Double[] m_i=edge[i][k].split_samples();
      Double[] m_j=edge[j][k].split_samples();
      if(m_i!=null && m_j!=null){
        d=d+m_i[0]*m_i[1]+m_j[0]*m_j[1]-m_i[0]*m_j[0]-m_i[1]*m_j[1];
        n++;
      }
    }
    return d/n;
  }
  
}
