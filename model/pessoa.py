from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from  model import Base, Comentario

class Pessoa(Base):
   __tablename__ = 'pessoa' 

   id = Column("id", Integer, primary_key=True)
   nome = Column(String(140), unique=True)
   telefone = Column(String(140))
   anotacao = Column(String(4000))
   cep = Column(String(140))
   logradouro = Column(String(140))
   bairro = Column(String(140))
   cidade = Column(String(140))
   uf = Column(String(20))
   data_insercao = Column(DateTime, default=datetime.now())
    # Definição do relacionamento entre o livro e o comentário.
   comentario = relationship("Comentario")
   def __init__(self, nome:str,telefone:str, anotacao:str,
                cep:str,logradouro:str,
               bairro:str, 
               cidade:str,uf:str,data_insercao:Union[DateTime, None] = None):
        """
        Cadastra uma Produto

        Arguments:
        nome: nome da pessoa
        telefone: telefone da pessoa.
        anotacao: Anotações para adicionar
        cep: cep da pessoa
        logradouro:logradouro
        bairro:bairro
        cidade: cidade da pessoa
        uf:uf
            data_insercao: data de quando a pessoa foi inserido à base
        """
        self.nome = nome
        self.telefone=telefone
        self.anotacao = anotacao
        self.cep=cep
        self.logradouro=logradouro
        self.bairro=bairro
        self.cidade=cidade
        self.uf=uf
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
   def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário 
        """
        self.comentarios.append(comentario)        