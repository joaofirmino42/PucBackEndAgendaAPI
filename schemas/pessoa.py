from pydantic import BaseModel
from typing import Optional, List
from model.pessoa import Pessoa
from schemas import ComentarioSchema

class PessoaSchema(BaseModel):
     """Define como uma nova pessoa a ser inserida deve ser representado"""
     nome: str="João Neto"
     telefone: str="21982861748"
     anotacao: str="Lembrar de ir na academia"
     cep: str="22461220"
     logradouro:str="Rua Professor Saldanha"
     bairro:str="Lagoa"
     cidade:str="Rio de Janeiro"
     uf:str="RJ"
class PessoaBuscaSchema(BaseModel):
     """
Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da pessoa.
     """
     nome:str="João Neto"
class ListagemPessoaSchema(BaseModel):
     """ Define como uma listagem de pessoas será retornada."""
     pessoas: List[PessoaSchema]
def apresenta_pessoas(pessoas: List[Pessoa]):
     """
     Retorna uma representação da pessoa seguindo o schema definido em
      PessoaViewSchema.
     """
     result = []
     for pessoa in pessoas:
          result.append({
               "nome":pessoa.nome,
               "telefone":pessoa.telefone,
               "anotacao": pessoa.anotacao,
               "cep": pessoa.cep,
               "logradouro": pessoa.logradouro,
               "bairro": pessoa.bairro,
               "cidade": pessoa.cidade,
               "anotacao": pessoa.uf,
              
          })

          return {"pessoas":result}
class PessoaViewSchema(BaseModel):
     """Define como uma pessoa será retornada"""
     id: int=1
     nome: str="João Neto"
     telefone: str="21982861748"
     anotacao: str="Lembrar de ir na academia"
     cep: str="22461220"
     logradouro:str="Rua Professor Saldanha"
     bairro:str="Lagoa"
     cidade:str="Rio de Janeiro"
     uf:str="RJ"
     total_cometario: int = 1
     comentario:List[ComentarioSchema]       
class PessoaDelSchema(BaseModel):
    
   
    nome:str

def apresenta_pessoa(pessoa:Pessoa):
     """
     Retorna uma representação da pessoa seguindo o schema definido em
      PessoaViewSchema.
     """
     return{
          "id": pessoa.id,
           "nome":pessoa.nome,
           "telefone":pessoa.telefone,
           "anotacao": pessoa.anotacao,
           "cep": pessoa.cep,
           "logradouro": pessoa.logradouro,
           "bairro": pessoa.bairro,
           "cidade": pessoa.cidade,
           "anotacao": pessoa.uf,
          "total_cometario": len(pessoa.comentario),
          "comentario": [{"texto": c.texto} for c in pessoa.comentario]
     }