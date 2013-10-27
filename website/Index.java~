import java.io.*;

public class Index{
  int MAX_PERPAGE = 30;
  public String head = "";
  public String body = "";
  public DB db = null;
  public String filename = null;
 
  public Index(DB db){
    this.db = db;
    this.filename = "index.html";
  }
  
  public void get_head(){
    String text = "";
    text += "<!DOCTYPE html> \n";
    text += "<html lang=\"en\"> \n";
    text += "<head> \n";
    text += "<meta charset=\"utf-8\"> \n";
    text += "<link rel=\"stylesheet\" href=\"indexstyles.css\"> \n";
    text += "</head> \n";   
    this.head=text;
  }
  
  public String get_politico(Deputado deputado){
    String current=null;
    try{
      current = new java.io.File( "." ).getCanonicalPath();
    }catch (Exception e){//Catch exception if any
      System.err.println("Cannot find current path. Error: " + e.getMessage());
    } 
     
    String picture_file = current+"/image/deputado/"+deputado.idecadastro+".jpg";
    
    String text="";
    
    text += "<article class=\"politicoblock\"> \n";
    text += "<figure> \n";
    text += "<img src=\""+picture_file+"\">";
    text += "</figure> \n";
    text += deputado.nomeparlamentar+"\n";
    text += "</article> \n";
    return(text);
  }
  
  public void get_body(){
    String text = "";
   
    text += "<body> \n";
    text += "<header> \n";
    text += "<h1> DEPUTADOS </h1> \n";
    text += "</header> \n";
    text += "<section id=\"mainsection\"> \n";
    
    for(int i=0; i<MAX_PERPAGE;i++){
       
      Deputado deputado = (Deputado) db.deputados.get(i+1);
    
      text += this.get_politico(deputado);
       
    }
    text += "</section> \n";
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
      System.err.println("Cannot write in file. Error: " + e.getMessage());
    }
    return(page);
  }
  
}