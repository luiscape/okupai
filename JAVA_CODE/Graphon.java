import java.util.*;
 

/*
 *Class Graphon 
 * 
 */
public class Graphon{
  
  public Double[][] w; //probability matrix
  public Graph g; //observations
  public Kernels ker; //kernel
  private Random rand = new Random(); 
 
  
  /*
   * Graphon(Graph g): generates a Graphon from the observations in Graph g 
   */
  public Graphon(Graph g){
    this.g=g;
  } 
  
    /*
   * Graphon(Graph w): generates a Graphon from surface matrix w
   */
  public Graphon(int nobs, Double[][] w){
    this.w=w;
    int size = w[0].length;
    this.get_observations(nobs,this.w);
  }
  
  /*
   * Graphon (int size, int nobs, int ker_ID, int param): generate graphons from specified
   * size of the graph, number of observations, kernel, parameter for the kernel
   */ 
  public Graphon(int size, int nobs, int ker_ID, int param){
    this.ker= new Kernels(size,param);
    this.w=ker.get_surface(ker_ID);
    this.get_observations(nobs,this.w);
  }
  
  public void get_observations(int nobs, Double[][] w){
    int size=w[0].length;
    this.g = new Graph(size,nobs);
    for(int i=0;i<size;i++){
      for(int j=0;j<=i;j++){
        for(int t=0;t<nobs;t++){
          Double p= rand.nextDouble();
          int value;
          if (p>w[i][j])
            value=1;
          else
            value=0;
          g.add_obs(i,j,value);
        }
      }
    } 
  }
  
  
  
  

  
  
}