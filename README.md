# chask



![GitHub repo size](https://img.shields.io/github/repo-size/alehkiz/chask?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/alehkiz/chask?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/alehkiz/chask?style=for-the-badge)
![Github open issues](https://img.shields.io/github/issues/alehkiz/chask?style=for-the-badge)


Um CRM desenvolvido em Flask


### Melhorias futuras:

- [] Criar rotas;
- [] Modelos de banco de dados - 20%;
- [] Criar aplicação para gestão de reclamações;
- [] Camada de administração para:
    - [] Administração de usuários (criação, inativação, atualização);
    - [] Gerenciamento de entidades e clientes;

## 💻 Pré-requisitos

* versão mais recente de `python`
* Utilize um ambiente virtual: https://docs.python.org/3/tutorial/venv.html
* No ambiente virtual, instale as bibliotecas necessárias: `pip install -r requirements.txt`

## ☕ Subindo o servidor:

Para utilizar, siga estas etapas:

Na raiz do repositórico, inicie o ambiente virual e instale os pacotes necessários, e rode flask run.

Lembre-se que utilizamos o postgres, logo, você deverá ter criado, além de criar o banco de dados com o nome `chask` e `chask_dev` após criar o banco de dados, rode o comando `flask shell` e no terminal utilize o comando `db.create_all()`, saia e então rode `flask run`


## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.

[⬆ Voltar ao topo](#chask)<br>
