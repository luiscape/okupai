public class Deputado{
  public int id_deputado;
  public String idecadastro;
  public String idparlamentar;
  public String nome;
  public String nomeparlamentar;
  public String sexo;
  public String uf;
  public int id_partido;
  public String gabinete;
  public String anexo;
  public String fone;
  public String email;
  
  public Deputado(int id_deputado, String idecadastro, String idparlamentar, String nome, String nomeparlamentar,String sexo, String uf, int id_partido, String gabinete, String anexo, String fone, String email){
    this.id_deputado=id_deputado;
    this.idecadastro=idecadastro;
    this.idparlamentar=idparlamentar;
    this.nome=nome;
    this.nomeparlamentar=nomeparlamentar;
    this.sexo=sexo;
    this.uf=uf;
    this.id_partido=id_partido;
    this.gabinete=gabinete;
    this.anexo=anexo;
    this.fone=fone;
    this.email=email;
  }
}
