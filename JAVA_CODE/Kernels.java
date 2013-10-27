import java.util.*;
import java.util.concurrent.*;
import java.lang.Math;

public class Kernels{
  public int size;
  public Double[] u;
  private Random rand = new Random();
  
  private int nBlocks =1;
  private Double[][]  blocks_connection;
  
  public Kernels(int size,int nBlocks){
    this.size=size;
    this.u=new Double[size];
    for(int i=0;i<size;i++)
      this.u[i]=rand.nextDouble();
    Arrays.sort(this.u);
    
    this.nBlocks = nBlocks;
    if(nBlocks>0){
      this.blocks_connection=new Double[nBlocks][nBlocks];
      for (int i=0;i<nBlocks;i++){
        for(int j=0;j<=i;j++){
          Double p= rand.nextDouble();
          this.blocks_connection[i][j]=p;
          this.blocks_connection[j][i]=p;
        }
      }
    }
  }
  
  public Double[][] get_surface(int ker_ID){
    Double[][] M= new Double[this.size][this.size];
    for (int i=0;i<this.size;i++){
      for(int j=0;j<=i;j++){
        Double p=ker(this.u[i],this.u[j],ker_ID);
        M[i][j]=p;
        M[j][i]=p;
      }
    }
    return M;
  }
  
  public Double ker(Double ui, Double uj,int ker_ID){
    switch(ker_ID){
      case 1:
        return this.blockmodel(ui,uj);
      case 2:
        return this.ker2(ui,uj);
      case 3:
        return this.ker3(ui,uj);
      case 4:
        return this.ker4(ui,uj);
      case 5:
        return this.ker5(ui,uj);
    }
    return -1.0;
  }
  
  public Double blockmodel(Double ui,Double uj){
    Double block_size=(1.0/this.nBlocks);
    int pos_i = (int) (ui/block_size);
    int pos_j = (int) (ui/block_size);
    return blocks_connection[pos_i][pos_j];
  }
  
  public Double ker2(Double ui,Double uj){
    return (ui+uj)/2;
  }
  
  public Double ker3(Double ui,Double uj){
    return ui*uj;
  }
    
  public Double ker4(Double ui,Double uj){
    if(ui<uj)
      return ui;
    return uj;
  }
  
  public Double ker5(Double ui,Double uj){
    return 1.0/(1.0+Math.exp(-ui-uj));
  }
}
