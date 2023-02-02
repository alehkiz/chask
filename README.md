# chask



![GitHub repo size](https://img.shields.io/github/repo-size/alehkiz/chask?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/alehkiz/chask?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/alehkiz/chask?style=for-the-badge)
![Github open issues](https://img.shields.io/github/issues/alehkiz/chask?style=for-the-badge)


Um CRM desenvolvido em Flask

### Funcionalidades:

 - Times:
    - Gerenciamento de times;
    - Dashboard de produtividade;
 - Chats:
    - Fase 1: Somente mensagem por texto para tratamento de reclamações, individualizado por times.
        - Etapa 1 (enviar e receber mensagems e times) - 100%;
        - Adionar messagens como lidas. #TODO: Criar a lógica para leitura de mensagens sempre que enviada ao frontend do usuário.
        -- Criado o modelo de Estágio de Eventos (TicketStageEvent) para cada Ticket no qual cada usuário será responsável pela conclusão da etapa
 - Fluxo de cada reclamação:
    - A ideia é o acompanhamento do inicio ao fim, incluindo:
        - Cada reclamação é um ticket, que é separado por etapas, podendo ser concluído em algums pré-definidas.
        - Para cada etapas um funcionário fica responsável até a conclusão da etapa;
            - Cada etapa possuí um SLA para resposta;
        - Alertas sobre  estour do SLA serão emitidos;
        - Pesquisa de satisfação (nota) por email;
        - Dashboard para acompanhamento da resolutividade;
        - Acompanhamento individual (melhoria)
 - Segurança:
    - [x] Permitir que um usuários tenha apenas uma seção ativa

### Melhorias futuras:

- [x] frontend principal;
    - [] frontend adminstrador;
    - [] frondend clientes;
    - [] frontend chat - 50%;
- [] Criar rotas;
- [] Criar sistema de chat - 40%
- [] Modelos de banco de dados - 80%;
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
