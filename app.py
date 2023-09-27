from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from model import Session, Pessoa, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pessoa_tag = Tag(name="Pessoa", description="Adição, visualização e remoção de pessoas à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à uma pessoas cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.get('/pessoas',tags=[pessoa_tag],
        responses={"200": ListagemPessoaSchema, "404": ErrorSchema})
def get_pessoas():
    """
    Faz a busca por todas as Pessoas cadastradas

    Retorna uma representação da listagem de pessoas.
    """
    logger.debug(f"Coletando pessoas ")
    # criando conexão com a base
    session = Session()
    # fazendo busca
    pessoas = session.query(Pessoa).all()
    print(pessoas)
    if not pessoas:
        # se não há pessoas cadastradas
        return {"pessoas": []}, 200
    else:
        logger.debug(f"%d pessoas econtradas" % len(pessoas))
        # retorna a representação de pessoa
        print(pessoas)
        return apresenta_pessoas(pessoas), 200
@app.get('/pessoa',tags=[pessoa_tag],
        responses={"200": PessoaViewSchema, "404": ErrorSchema} ) 
def get_pessoa(query:PessoaBuscaSchema):
    """
    Faz a busca por uma Pessoa a partir do id da pessoa

    Retorna uma representação das pessoas e comentários associados.
    """
    nome=query.nome
    logger.debug(f"Coletando dados sobre a pessoa #{nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca 
    pessoa= session.query(Pessoa).filter(Pessoa.nome==nome).first()
    if not pessoa:
        # se a pessoa não foi encontrado
        error_msg = "Pessoa não encontrada na base :/"
        logger.warning(f"Erro ao buscar pessoa '{nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pessoa encontrado: '{pessoa.nome}'")
        # retorna pessoa
        return apresenta_pessoas(pessoa), 200
@app.delete('/pessoa', tags=[pessoa_tag],
             responses={"200": PessoaViewSchema, "404": ErrorSchema})
def del_pessoa(query:PessoaBuscaSchema):
    """
    Deleta uma pessoa a partir do id da pessoa informado

    Retorna uma mensagem de confirmação da remoção.
    """
    nome= unquote(unquote(query.nome))
    print(nome)
    logger.debug(f"Deletando dados sobre pessoa #{nome}")
    #criando conexão com a base
    session= Session()
    #fazendo remoção
    count= session.query(Pessoa).filter(Pessoa.nome==nome).delete()
    session.commit()
    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado pessoa #{nome}")
        return {"mesage": "pessoa removida", "id": nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Pessoa não encontrado na base :/"
        logger.warning(f"Erro ao deletar pessoa #'{nome}', {error_msg}")
        return {"mesage": error_msg}, 404    
@app.post('/pessoa',tags=[pessoa_tag],
          responses={"200": PessoaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pessoa(form: PessoaSchema):
    
    pessoa= Pessoa(
        nome=form.nome,
        telefone=form.telefone,
        anotacao=form.anotacao,
        cep=form.cep,
        logradouro=form.logradouro,
        bairro=form.bairro,
        cidade=form.cidade,
        uf=form.uf)
    logger.debug(f"Adicionando pessoa de nome: '{pessoa.nome}'")
    logger.debug(form)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(pessoa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado pessoa de nome: '{pessoa.nome}'")
        return apresenta_pessoa(pessoa), 200
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pessoa de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar pessoa '{pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pessoa '{pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
@app.put('/pessoas',tags=[pessoa_tag],
          responses={"200": PessoaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_pessoa(form: PessoaSchema):
    
    pessoa= Pessoa(
        nome=form.nome,
        telefone=form.telefone,
        anotacao=form.anotacao,
        cep=form.cep,
        logradouro=form.logradouro,
        bairro=form.bairro,
        cidade=form.cidade,
        uf=form.uf)
    logger.debug(f"Adicionando pessoa de nome: '{pessoa.nome}'")
    logger.debug(form)
    try:
        # criando conexão com a base
        session = Session()
        # atualizando pessoa
       
        session.query(Pessoa).filter(Pessoa.nome==pessoa.nome).update({pessoa},synchronize_session=False)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Atualizando pessoa de nome: '{pessoa.nome}'")
        return apresenta_pessoa(pessoa), 200
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pessoa de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar pessoa '{pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pessoa '{pessoa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
@app.post('/comentario', tags=[comentario_tag],
          responses={"200": PessoaViewSchema, "404":  ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """
     Adiciona  um novo comentário à uma pessoa cadastrada na base identificado pelo id

    Retorna uma representação das pessoas e comentários associados.
    """
    id  = form.id
    logger.debug(f"Adicionando comentários a pessoa #{id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    pessoa = session.query(pessoa).filter(Pessoa.id == id).first()

    if not pessoa:
        # se livro não encontrado
        error_msg = "Pessoa não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário a pessoa '{id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao livro
    pessoa.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário a pessoa #{id}")

    # retorna a representação de um livro
    return apresenta_pessoa(pessoa), 200
    