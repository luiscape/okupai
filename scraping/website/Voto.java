public class Voto{
  public int id_votacao;
  public String nome_deputado;
  public String partido_deputado;
  public String uf_deputado;
  public String voto;
  public int graph_vertex;
  
   public Voto(String nome_deputado, String partido_deputado, String uf_deputado, int graph_vertex){
    this.id_votacao = id_votacao;
    this.nome_deputado = nome_deputado;
    this.partido_deputado = partido_deputado;
    this.uf_deputado = uf_deputado;
    this.voto = null;
    this.graph_vertex = -1;
  }
  
  public Voto(int id_votacao, String nome_deputado, String partido_deputado, String uf_deputado, String voto, int graph_vertex){
    this.id_votacao = id_votacao;
    this.nome_deputado = nome_deputado;
    this.partido_deputado = partido_deputado;
    this.uf_deputado = uf_deputado;
    this.voto = voto;
    this.graph_vertex = graph_vertex;
  }
}