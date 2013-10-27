import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.*;


public class TransparenciaGraph
{
  String databaseFile = "jdbc:sqlite:../database/transparencia.db";

  public List votacao_list = new ArrayList();
  public Dictionary vertices = new Hashtable();
  public Dictionary partidos = new Hashtable();
  public String[] vertices_label=null;
  public String[] partidos_label=new String[2000];
  public int[][] results=null;
  
  
  //d.put("Thiago",1)
  //d.get("Thiago")
  
  public Connection connection = null;
  public Statement statement = null;
  public TransparenciaGraph()throws ClassNotFoundException
  {
    // load the sqlite-JDBC driver using the current class loader
    Class.forName("org.sqlite.JDBC");
    // Connection connection = null;
    try
    {
      // create a database connection
      this.connection = DriverManager.getConnection(databaseFile);
      this.statement = this.connection.createStatement();
      this.statement.setQueryTimeout(30);  // set timeout to 30 sec.
    }
    
    catch(SQLException e)
    {
      // if the error message is "out of memory", 
      // it probably means no database file is found
      
       try
       {
         if(connection != null)
           connection.close();
       }
       catch(SQLException e1)
       {
         // connection close failed.
         System.err.println(e1);
       }
       System.err.println(e.getMessage());
    }
  }
  
    public void get_vertices(String year){
    String query;
    List<Integer> ls=new ArrayList<Integer>();
   // query = "select distinct voto.nome_deputado,voto.partido_deputado,voto.uf_deputado from votacao join voto where"+
   //   " voto.id_votacao=votacao.id_votacao and  substr(votacao.data,-4)='"+ year +"'";
    query = "select distinct voto.partido_deputado from votacao join voto where"+
      " voto.id_votacao=votacao.id_votacao and  substr(votacao.data,-4)='"+ year +"'";
   
    try{
      ResultSet rs = this.statement.executeQuery(query);      
      while(rs.next())
      {
        String partido=rs.getString("partido_deputado");
      //  String label = rs.getString("nome_deputado")+partido+rs.getString("uf_deputado");
        String label=partido;
        //Voto v = new Voto(rs.getString("nome_deputado"),rs.getString("partido_deputado"),rs.getString("uf_deputado"),this.vertices.size());
        int nv=this.vertices.size();
        this.vertices.put(label,nv);
        partidos_label[nv]=partido;
      //  this.partidos.put(partido,nv);
        
//        System.out.println("deputado "+this.vertices.size()+":"+label);
      }
      
      int nVertex=this.vertices.size();
      vertices_label= new String[nVertex];
    //  partidos_label= new String[nVertex];
      
      
      Enumeration keys = this.vertices.keys();
      while(keys.hasMoreElements()){
        String nome=(String) keys.nextElement();
        int pos = (int) vertices.get(nome);
        vertices_label[(int) vertices.get(nome)]=nome; 
      }
      
 /*     Enumeration keys2 = this.partidos.keys();
      while(keys2.hasMoreElements()){
        String nome=(String) keys2.nextElement();
        
        System.out.println(partidos_label.get(nome)+ " "+nome);
        partidos_label[(int) partidos.get(nome)]=nome; 
      }
      
  */   
      
      
      
    }catch(SQLException e1)
    {
      System.err.println(e1);
    } 
    
    
  }
  
  
  
  public void get_votacao(String year){
    String query;
    List<Integer> ls=new ArrayList<Integer>();
//    query = "select distinct voto.id_votacao  from proposicoes join votacao join voto where"+
//      " voto.id_votacao=votacao.id_votacao and votacao.id_proposicao=proposicoes.id_proposicao and proposicoes.ano="+ year +"";
    query = "select distinct voto.id_votacao  from votacao join voto where"+
      " voto.id_votacao=votacao.id_votacao and  substr(votacao.data,-4)='"+ year +"'";

    
    try{
      ResultSet rs = this.statement.executeQuery(query);      
      while(rs.next())
      {
        String id_votacao = rs.getString("id_votacao");
        votacao_list.add(id_votacao);
//        System.out.println("votacao "+id_votacao);
      }
    }catch(SQLException e1)
    {
      System.err.println(e1);
    } 
    
  }
  
  public int[] get_votos(String id_votacao){
    String query;
    query = "select *  from voto where voto.id_votacao="+ id_votacao +"";
    int nVertex=this.vertices.size();
    int[] votos = new int[nVertex]; //1=Sim,0=Nao,-1=qualuqer outra coisa
    for(int i =0;i<nVertex;i++){
     votos[i]=-2; 
    }
    try{
      ResultSet rs = this.statement.executeQuery(query); 
      int simCount = 0;
      int naoCount = 0;
      while(rs.next())
      {
        String partido_deputado = rs.getString("partido_deputado");
        Boolean isGov = false;
        if(partido_deputado.compareTo("PT")==0)
          isGov=true;
        
    //    String label = rs.getString("nome_deputado")+rs.getString("partido_deputado")+rs.getString("uf_deputado");
         String label = rs.getString("partido_deputado");
        int vertex_index = (int) (this.vertices).get(label);
        String voto =rs.getString("voto");
        
        votos[vertex_index]=-1;
        if(voto.compareTo("N�o")==0){
         votos[vertex_index]=0;
         if(isGov)
           naoCount++;
        }
        if(voto.compareTo("Sim")==0){
          votos[vertex_index]=1;
          if(isGov)
            simCount++;
        }
        
//        System.out.println(voto+"  "+votos[vertex_index] + " "+partido_deputado+" "+isGov);
      }
      int ptVote =0;
      if (simCount>naoCount)
        ptVote=1;
//      System.out.println("Sim:"+simCount+" "+"Nao:"+naoCount+" .. voto PT:"+ptVote);
      
      int[] voto_PT = new int[nVertex]; //1=igual a PT,0=diferente de PT
      
     
      for(int i =0;i<nVertex;i++){
        voto_PT[i]=-1;
        if(votos[i]==ptVote)
          voto_PT[i] = 1; 
        else if (votos[i]>=0){
          voto_PT[i]=0;
        }
      }
      
/*      String results = "";
      String results_vote="";
      for(int i =0;i<nVertex;i++){
       results=results+" "+voto_PT[i];
       results_vote=results_vote+" "+votos[i];
      }   
      System.out.println(results);
      System.out.println(results_vote);
*/      
      return(voto_PT);
    }catch(SQLException e1)
    {
      // connection close failed.
      System.err.println(e1);
    }  
    return(null);
    
  }
  
  public void run(String year){
    
    this.get_vertices(year);
    this.get_votacao(year);
    
    this.results = new int[votacao_list.size()][vertices.size()];
    
    Iterator it = votacao_list.iterator();
    int id_votacao;
    int count = 0;
    while(it.hasNext()){
     String id_vot=(String) it.next();
   // System.out.println("Votacao "+id_vot);
     this.results[count]=this.get_votos(id_vot);
     count ++;
    }

    
 // List votacao_list = new ArrayList();
 // public Dictionary vertices = new Hashtable();
    
    
    
  //  Enumeration e = t.vertices.keys();
   // e.nextElement();
    
  }
  
 
  
}

