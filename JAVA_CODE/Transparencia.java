import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.*;


public class Transparencia
{
  
  
  
  
  public static void main(String[] args) throws ClassNotFoundException
  {
    // load the sqlite-JDBC driver using the current class loader
    Class.forName("org.sqlite.JDBC");
    
    Connection connection = null;
    try
    {
      // create a database connection
      connection = DriverManager.getConnection("jdbc:sqlite:../database/transparencia.db");
      Statement statement = connection.createStatement();
      statement.setQueryTimeout(30);  // set timeout to 30 sec.
      
      int id_votacao = 4;
      
      String query;
      query = "select *  from voto where voto.id_votacao="+ id_votacao;
      
    //  query = "Select  from voto where voto.id_votacao="+id_votacao;
     
      ResultSet rs = statement.executeQuery(query);
      
         
   //   ResultSet rs = statement.executeQuery("select * from voto");
      
      
      while(rs.next())
      {
        // read the result set
        System.out.println("name = " + rs.getString("nome_deputado"));
 //       System.out.println("id = " + rs.getInt("id"));
      }
    }
    catch(SQLException e)
    {
      // if the error message is "out of memory", 
      // it probably means no database file is found
      System.err.println(e.getMessage());
    }
    finally
    {
      try
      {
        if(connection != null)
          connection.close();
      }
      catch(SQLException e)
      {
        // connection close failed.
        System.err.println(e);
      }
    }
  }
}