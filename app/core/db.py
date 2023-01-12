import click
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore
from flask.cli import with_appcontext
from datetime import datetime
from flask import current_app as app

db =SQLAlchemy(session_options={'autoflush':False})

from app.models.secutiry import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

@click.command('populate-db')
@with_appcontext
def populate_db_command():
    """Clear the existing data and create new tables."""
    
    # time.sleep(10)
    
    # from app.models.secutiry import User, Role
    # from app.models.network import Network
    # from app.models.comment import Comment
    # from app.models.ticket import Ticket, TicketType
    from app.models import get_class_models
    for k, v in get_class_models().items():
        globals()[k] = v # Add all models to globals # Force import
    db.drop_all()
    db.create_all(app=app)
    click.echo('Banco de dados inicializado...')
    network = Network.query.filter(Network.ip == '0.0.0.0').first()
    if network is None:
        network = Network()
        network.ip = '0.0.0.0'
        db.session.add(network)
        db.session.commit()
    ticket_type = TicketType.query.filter(TicketType.type == 'Teste').first()
    if ticket_type is None:
        ticket_type = TicketType()
        ticket_type.type = "Teste"
        db.session.add(ticket_type)
        db.session.commit()
        click.echo(f'TicketType criado com sucesso id: {ticket_type.id}')
    ticket = Ticket.query.filter(Ticket.name == 'Teste').first()
    if ticket is None:
        ticket = Ticket()
        ticket.name = 'Teste'
        ticket.info = 'Apenas um teste sobre ticket'
        ticket.deadline = datetime.now()
        ticket.type_id = ticket_type.id
        ticket.network_id = network.id
        db.session.add(ticket)
        db.session.commit()
        click.echo(f'Ticket criado com sucesso id: {ticket.id}')
    user = User.query.filter(User.username == 'admin').first()
    if user is None:
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
        click.echo(f'User criado com sucesso id: {user.id}')

    comment = Comment.query.filter(Comment.text == 'Teste de comentário').first()
    if comment is None:
        comment = Comment()
        comment.ticket_id = ticket.id
        comment.user_id = user.id
        comment.text = 'Teste de comentário'
        comment.create_network_id = network.id
        db.session.add(comment)
        db.session.commit()
        click.echo(f'Comment criado com sucesso id: {comment.id}')

    click.echo('Finalizado')