public class Main{
 
  public static void main(String[] args){
    
    try{
      DB db = new DB();
      db.run();
 /*     Deputado deputado = (Deputado) db.deputados.get(1);
      Page_deputado_profile pg = new Page_deputado_profile(deputado);
      pg.get_page(); */
      

      
      Index ind = new Index(db);

      ind.get_page();
      
    }catch (Exception e){//Catch exception if any
      System.err.println("Error Main: " + e.getMessage());
    }
    
  }
  
}

  