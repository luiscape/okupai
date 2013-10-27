public class Edge{
  public int row;
  public int col;
  public int[] obs;
  public int nobs;
  

  public Edge(int row,int col, int max_obs){
    this.row=row;
    this.col=col;
    this.obs = new int[max_obs];
    for (int i=0;i<max_obs;i++)
    {
     this.obs[i]=-1;
    }
    this.nobs=0;
  }
  
  public void add_obs(int value) {
//    System.out.println("Adding edge "+this.row+"-"+this.col+" ___ "+value);
   this.obs[this.nobs]=value;
   this.nobs++;
  }
  
  public Double[] split_samples(){
  
    if (this.nobs <2)
      return null;
    
    int half_obs = (this.nobs+1)/2;
    Double[] m = new Double[2];
    m[0]=0.0;
    m[1]=0.0;
 
    for (int i =0;i<half_obs;i++)
    {
      m[0]=m[0]+this.obs[i];
    }
    m[0]=m[0]/half_obs;
    
    for (int i=half_obs;i<this.nobs;i++)
    {
      m[1]=m[1]+this.obs[i];
    }
    m[1]=m[1]/(nobs-half_obs);
    
    return m;
  }
  
}