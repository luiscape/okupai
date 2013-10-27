import java.io.*;

public class Page_deputado_profile{
  public String head = "";
  public String body = "";
  public Deputado deputado = null;
  public String picture_file = "";
  public String filename = null;
 
  

  
  

  public Page_deputado_profile(Deputado deputado){
    this.deputado=deputado;
    String current = null;
    try{
      current = new java.io.File( "." ).getCanonicalPath();
    }catch (Exception e){//Catch exception if any
      System.err.println("Error: " + e.getMessage());
    } 
    
    this.picture_file = current+"/image/deputado/"+deputado.idecadastro+".jpg";
    this.filename = "profiles/"+deputado.idecadastro+".html";
  }
  
  public void get_head(){
    String text = "";
    text += "<!DOCTYPE html> \n";
    text += "<html lang=\"en\"> \n";
    text += "<head> \n";
    text += "<meta charset=\"utf-8\"> \n";
    text += "</head> \n";   
    this.head=text;
  }
  
  public void get_body(){
    String text = "";
   
    text += "<body> \n";
    text += "<header> \n";
    text += "<h1> DEPUTADOS </h1> \n";
    text += "</header> \n";
    
    text += "Oi oi oi";
    text += "<figure>";
    text += "<img src=\""+this.picture_file+"\">";
    text += "</figure>";
    
    text += "</body> \n"; 
    text += "</html> \n";
   
    this.body = text;
  }
  
  
  
  public String get_page(){
    this.get_head();
    this.get_body();
    String page = this.head+this.body; 
    try{
      FileWriter fstream = new FileWriter(this.filename);
      BufferedWriter out = new BufferedWriter(fstream);
      out.write(page);
      out.close();
    }catch (Exception e){//Catch exception if any
      System.err.println("Error: " + e.getMessage());
    }
    return(page);
  }
  
}