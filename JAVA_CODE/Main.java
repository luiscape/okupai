import java.io.*;

public class Main{
 
  public static void main(String[] args){
    Double delta = 0.0001;
 //   Graphon g = new Graphon(200,5,1,10);
 //   GraphonEstimator estimator = new GraphonEstimator(g.g);
 //   estimator.get_clusters(delta);
    try{
      
      TransparenciaGraph t = new TransparenciaGraph();
      t.run("2011");
      System.out.println("Estimating Graphon");
      
      System.out.println(t.results.length+"  "+t.results[0].length);
      GraphonEstimator ge = new GraphonEstimator(t.results);
      System.out.println("Getting clusters");
      ge.get_clusters(delta);
      System.out.println("Printing clusters");
      System.out.println(ge.clusters.length);
      
      int nclusters = ge.nclusters;
      String[] clusters = new String[nclusters];
      
      for(int i=0;i<nclusters;i++){
       clusters[i]="";
       
      }
      for(int i = 0;i<ge.clusters.length;i++){
        int cl=ge.clusters[i];
        clusters[cl]=clusters[cl]+" "+t.partidos_label[i];
      }
      for(int i=0;i<nclusters;i++){
        System.out.println("");
        System.out.println("..............  Cluster "+i+"   .................");
       System.out.println(clusters[i]);
      }
    }
    catch(Exception e)
    {
      System.out.println("Deu erro");
      // if the error message is "out of memory", 
      // it probably means no database file is found
      System.err.println(e.getMessage());
    }
    
  }
  
}
  
  