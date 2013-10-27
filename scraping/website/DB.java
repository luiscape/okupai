import java.sql.Connection; 
import java.sql.DriverManager; 
import java.sql.ResultSet; 
import java.sql.SQLException; 
import java.sql.Statement; 
import java.util.*; 
 
 
public class DB 
{ 
  String databaseFile = "jdbc:sqlite:../database/transparencia.db"; 
 
  public List votacao_list = new ArrayList(); 
  public Dictionary deputados = new Hashtable(); 
  public Dictionary partidos = new Hashtable(); 

   
   
  public Connection connection = null; 
  public Statement statement = null; 
  public DB()throws ClassNotFoundException 
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
   
   
    public void get_partidos(){
      String query = "select * from partido"; 
      try{
        ResultSet rs = this.statement.executeQuery(query);      
        while(rs.next())
        {
          Integer id_partido= Integer.parseInt(rs.getString("id_partido"));
          String nome = rs.getString("nome");
          String sigla = rs.getString("sigla");
          Partido partido = new Partido(id_partido,nome,sigla);
          this.partidos.put(id_partido,partido);
        }   
      }catch(SQLException e1)
      {
        System.err.println(e1);
      }
      /*
      Enumeration e = this.partidos.elements();
      while(e.hasMoreElements()){
        Partido partido = (Partido) e.nextElement(); 
        System.out.println(partido.nome);
      }*/
    }
    
    
    public void get_deputados(){
      String query = "select * from deputado"; 
      try{
        ResultSet rs = this.statement.executeQuery(query);      
        while(rs.next())
        {

          int id_deputado=Integer.parseInt(rs.getString("id_deputado"));
          String idecadastro=rs.getString("idecadastro");
          String idparlamentar=rs.getString("idparlamentar");
          String nome=rs.getString("nome");
          String nomeparlamentar=rs.getString("nomeparlamenter");
          String sexo=rs.getString("sexo");
          String uf=rs.getString("uf");
          int id_partido=Integer.parseInt(rs.getString("id_partido"));
          String gabinete=rs.getString("gabinete");
          String anexo=rs.getString("anexo");
          String fone=rs.getString("fone");
          String email=rs.getString("email");
      
          Deputado deputado = new  Deputado(id_deputado,idecadastro,idparlamentar,nome,nomeparlamentar,sexo,uf,id_partido,gabinete,anexo,fone,email);
       
          this.deputados.put(id_deputado,deputado);
        }   
      }catch(SQLException e1)
      {
        System.err.println(e1);
      }
      
      /* PRINTING RESUlT
      Enumeration e = this.deputados.elements();
      while(e.hasMoreElements()){dg.
        Deputado dep = (Deputado) e.nextElement();
         System.out.println("     ...        ");
        System.out.println(dep.id_deputado);
        System.out.println(dep.idecadastro);
        System.out.println(dep.idparlamentar);
      }*/
    }
    
  public void run(){ 
    this.get_deputados();
    this.get_partidos();    
  } 
   
} 
 
