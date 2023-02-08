import click
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore
from flask.cli import with_appcontext
from datetime import datetime
from flask import current_app as app

db =SQLAlchemy(session_options={'autoflush':False})

from app.models.security import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

@click.command('init-db')
@with_appcontext
def init_db():
    from app.models import get_class_models
    for k, v in get_class_models().items():
        globals()[k] = v # Add all models to globals # Force import
    db.create_all()
    stages = []
    stages_name = ['Criado', 'Vinculado', 'Em análise', 'Indevido', 'Transferido', 'Finalizado']
    for idx, name in enumerate(stages_name):
        ts = TicketStage.query.filter(TicketStage.name == name).first()
        if ts != None:
            continue
        ts = TicketStage()
        ts.name = name
        ts.level = idx
        stages.append(ts)
    db.session.add_all(stages)
    db.session.commit()
    click.echo('Estágios de ticket criados.')

@click.command('fake-db')
@with_appcontext
def fake_db_command():
    """Clear the existing data and create new tables with fake data"""
    if app.config['ENV'] != 'development':
        click.echo('Não é possível popular dados de testes em produção')
        return False
    # time.sleep(10)
    
    # from app.models.secutiry import User, Role
    # from app.models.network import Network
    # from app.models.comment import Comment
    # from app.models.ticket import Ticket, TicketType
    from faker import Faker
    from random import choice, randint
    from datetime import datetime, timedelta
    from app.models import get_class_models
    faker = Faker(locale='pt_BR')
    for k, v in get_class_models().items():
        globals()[k] = v # Add all models to globals # Force import
    db.drop_all()
    db.create_all()
    click.echo('Banco de dados inicializado...')
    network = Network()
    network.ip = '0.0.0.0'
    db.session.add(network)
    db.session.commit()
    user = User()
    user.name = 'admin'
    user.username = 'admin'
    user.email = 'admin@localhost'
    user.password = 'Abc123'
    user.active = True
    user.temp_password = False
    user.created_network_id = network.id
    db.session.add(user)
    db.session.commit()
    click.echo(f'Administrador criado com sucesso id: {user.id}')
    reclamacao = TicketType()
    reclamacao.type = 'Reclamação'
    pedido = TicketType()
    pedido.type = 'Pedido'
    tickets_type = [reclamacao, pedido]
    db.session.add_all(tickets_type)
    db.session.commit()
    click.echo(f'TicketType criados: \nReclamação: {reclamacao.id} \nPedido: {pedido.id}')
    roles = []
    admin = Role()
    admin.name = "admin"
    admin.level = 0
    roles.append(admin)
    local_admin = Role()
    local_admin.name = 'local_admin'
    local_admin.level = 1
    roles.append(local_admin)
    support = Role()
    support.name = 'support'
    support.level = 3
    roles.append(support)
    db.session.add_all(roles)
    db.session.commit()
    click.echo(f'Roles criadas')
    #lists
    networks = []
    users = []
    # roles = []
    # tickets_type = []
    tickets = []
    addresses = []
    addresses_type = []
    cities = []
    states = []
    postcodes = []
    costumers = []
    contacts = []
    comments = []
    messages = []

    for _ in range(1000):
        network = Network()
        network.ip = faker.ipv4()
        networks.append(network)
        # db.session.add(network)
    
    db.session.add_all(networks)
    db.session.commit()
    usernames = []
    emails = []
    for _ in range(100):
        _user = User()
        username = faker.user_name()
        while username in usernames:
            username = faker.user_name()  
        usernames.append(username)
        _user.username = username
        _user.name = faker.name()
        email = faker.email()
        while email in emails:
            email = faker.email()
        _user.email = email
        _user.password = 'Abc123'
        _user.active = True
        _user.temp_password = False
        _user.created_network_id = choice(networks).id
        _user.roles.append(choice(roles))
        users.append(_user)
    db.session.add_all(users)
    db.session.commit()
    click.echo('Usuários criados com sucesso')
    preffixes = []
    for _ in range(100):
        preffix = faker.street_prefix()
        # at = AddressType.query.filter(AddressType.type == preffix).first()
        if not preffix in preffixes:
            at = AddressType()
            at.type = preffix
            addresses_type.append(at)
            preffixes.append(preffix)
    db.session.add_all(addresses_type)
    db.session.commit()
    click.echo('Tipos de endereço criados com sucesso')

    cpf = CostumerIdentifierType()
    cpf.type = 'CPF'
    db.session.add(cpf)
    db.session.commit()

    states_dic = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins'
    }
    for key, value in states_dic.items():
        state = StateLocation()
        state.state = value
        state.uf = key
        states.append(state)
    db.session.add_all(states)
    db.session.commit()
    click.echo('Estados criados com sucesso')
    city_names = []
    for _ in range(100):
        city_name = faker.city()
        if not city_name in city_names:
            city = City()
            city.city = city_name
            city.uf_id = choice(states).id
            cities.append(city)
            city_names.append(city_names)
    db.session.add_all(cities)
    db.session.commit()
    click.echo('Cidades criadas com sucesso')
    codes = []
    for _ in range(100):
        postcode = faker.postcode()
        
        if not postcode in codes:
            code = AddressPostcode()
            code.code = postcode
            postcodes.append(code)
            codes.append(code)
    db.session.add_all(set(postcodes))
    db.session.commit()
    click.echo('Códigos postais criados com sucesso')


    for _ in range(100):
        ad = Address()
        ad.name = faker.street_name()
        ad.postcode_id = choice(postcodes).id
        ad.address_type_id = choice(addresses_type).id
        ad.number = int(faker.building_number())
        ad.city_id = choice(cities).id
        addresses.append(ad)

    db.session.add_all(addresses)
    db.session.commit()
    click.echo('Códigos postais criados com sucesso')
    

    for _ in range(100):
        contact = Contact()
        contact.phone_principal = faker.cellphone_number()
        contact.phone_secondary = faker.cellphone_number()
        contacts.append(contact)

    db.session.add_all(contacts)
    db.session.commit()
    click.echo('contatos criados com sucesso')


    for _ in range(100):
        costumer = Costumer()
        costumer.name = faker.name()
        costumer.identifier_type_id = cpf.id
        costumer.identifier = faker.cpf()
        costumer.contact_id = choice(contacts).id
        costumer.address_id = choice(addresses).id
        costumers.append(costumer)

    db.session.add_all(costumers)
    db.session.commit()
    click.echo('Clientes criados com sucesso')

    groups_services = []
    groups = ['Habilitação', 'Veículos']
    for _g in groups:
        gs = GroupService()
        gs.name = _g
        groups_services.append(gs)
    db.session.add_all(groups_services)
    db.session.commit()
    click.echo('Grupos criados com sucesso')

    services = []
    for _ in range(50):
        s = Service()
        s.group_id = choice(groups_services).id
        s.name = faker.text(max_nb_chars=20).replace('.','').replace(' ', '')
        services.append(s)

    db.session.add_all(services)
    db.session.commit()
    click.echo('Serviços criados com sucesso')


    for _ in range(100):
        _ticket = Ticket()
        _ticket.name = faker.text(max_nb_chars=500)
        _ticket.title = faker.text(max_nb_chars=20)
        _ticket.info = faker.text(max_nb_chars=5000)
        _ticket.deadline = faker.date_between_dates(datetime.today(), datetime.today() + timedelta(days=365))
        _ticket.type_id = choice(tickets_type).id
        _ticket.create_network_id = choice(networks).id
        _ticket.create_user_id = choice(users).id
        _ticket.costumer_id = choice(costumers).id
        _ticket.service_id = choice(services).id
        tickets.append(_ticket)
    db.session.add_all(tickets)
    db.session.commit()
    click.echo('Tickets criados com sucesso')
    
    # users_tickets = []
    # for _ticket in Ticket.query:
    #     ut = UserTicket()
    #     ut.user_id = choice(users).id
    #     ut.ticket_id = _ticket.id
    #     users_tickets.append(ut)
    # db.session.add_all(users_tickets)
    # db.session.commit()

    for _ in range(3000):
        _cm = Comment()
        _cm.ticket_id = choice(tickets).id
        _cm.user_id = choice(users).id
        _cm.text = faker.text(max_nb_chars=5000)
        _cm.create_network_id = choice(networks).id
        comments.append(_cm)
    db.session.add_all(comments)
    db.session.commit()
    click.echo('Comentários criados com sucesso')
    comments2 = []
    for _ in range(3000):
        _cm = Comment()
        _cm.ticket_id = choice(tickets).id
        _cm.user_id = choice(users).id
        _cm.text = faker.text(max_nb_chars=5000)
        _cm.create_network_id = choice(networks).id
        _cm.comment_id = choice(comments).id
        comments2.append(_cm)
    db.session.add_all(comments2)
    db.session.commit()
    click.echo('Respostas de Comentários criados com sucesso')
    
    # groups = []
    # groups_name = []
    # for _ in range(10):
    #     group_name = faker.text(max_nb_chars=10).replace('.','').replace(' ', '')
    #     if not group_name in groups_name:
    #         group = GroupChat()
    #         group.name = group_name
    #         groups.append(group)
    #         groups_name.append(group_name)
    # db.session.add_all(groups)
    # db.session.commit()
    # click.echo('Grupos criados com sucesso')
    teams = []
    for _ in range(200):
        t =Team()
        t.name = faker.text(max_nb_chars=randint(20,30))
        t.active = True
        teams.append(t)
    db.session.add_all(teams)
    db.session.commit()

    for _ in range(1000):
        ms = Message()
        ms.message = faker.text(max_nb_chars=randint(50,999))
        ms.user_sender_id = choice(users).id
        ms.user_destiny_id = choice(users).id
        ms.create_network_id = choice(networks).id
        ms.team_id = choice(teams).id
        messages.append(ms)
    db.session.add_all(messages)
    db.session.commit()
    click.echo('Mensagens criadas com sucesso')

    messages2 = []
    for _ in range(1000):
        ms = Message()
        ms.message = faker.text(max_nb_chars=randint(50,999))
        ms.user_sender_id = choice(users).id
        ms.user_destiny_id = choice(users).id
        ms.create_network_id = choice(networks).id
        ms.message_id = choice(messages).id
        messages2.append(ms)
    db.session.add_all(messages2)
    db.session.commit()
    click.echo('Respostas de mensagem criadas com sucesso')
    
    # for _ in range(900):
    #     group = choice(groups)
    #     for x in range(10):
    #         group.users.append(choice(users))
    # db.session.commit()
    
    

    
    users =User.query.all()
    admin = User.query.filter(User.username == 'admin').first()
    for t in Team.query.all():
        t.administrators.append(admin)
        for _ in range(30):
            _adm = choice(users)
            _user = choice(users)
            if not _adm in t.administrators:
                t.administrators.append(_user)
            if not _user in t.users:
                t.users.append(choice(users))
    db.session.commit()
    click.echo('Finalizado')