from flask import current_app as app, flash
from datetime import date, datetime

from sqlalchemy import Date, asc, cast, extract, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import db
from app.models.base import BaseModel
from app.models.network import Network
from app.models.security import User
from app.utils.datetime import convert_datetime_to_local


class Page(BaseModel):
    __abstract__ = False
    endpoint = db.Column(db.String, unique=True, nullable=False)
    route = db.Column(db.String, unique=True, nullable=False)
    visit = db.relationship('Visit', cascade='all, delete-orphan',
                            single_parent=True, backref='page', lazy='dynamic')

    def add_view(self, user_id, network_id):
        
        
        user = User.query.filter(User.id == user_id).first()
        
        visit = Visit()
        visit.page_id = self.id
        if user is None:
            visit.user_id = None
        else:
            visit.user_id = user.id
        visit.network_id = network_id
        visit.datetime = datetime.utcnow()
        db.session.add(visit)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
            app.logger.error(e)
            db.session.rollback()
            flash('Não foi possível atualizar a visualização', category='warning')
        return visit


class Visit(BaseModel):
    __abstract__ = False
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    page_id = db.Column(UUID(as_uuid=True), db.ForeignKey('page.id'), nullable=False)
    network_id = db.Column(UUID(as_uuid=True), db.ForeignKey('network.id'), nullable=False)


    @staticmethod
    def query_by_month_year(year: int, month: int):
        return Visit.query.filter(extract('year', Visit.datetime) == year, extract('month', Visit.datetime) == month)

    @staticmethod
    def query_by_year(year: int):
        return Visit.query.filter(extract('year', Visit.datetime) == year)

    @staticmethod
    def query_by_date(date: date):
        return Visit.query.filter(cast(Visit.datetime, Date) == date)

    @staticmethod
    def query_by_interval(start: date, end: date):
        return Visit.query.filter(cast(Visit.datetime, Date) == start, cast(Visit.datetime, Date) == end)

    @staticmethod
    def total_by_date(start: str, end: str):
        start = datetime.strptime(start, '%d-%m-%Y')
        end = datetime.strptime(end, '%d-%m-%Y')
        # timedelta = (end - start).days
        # if timedelta > 60:
        #     raise Exception('Intervalo de datas maior que 60 dias')
        return db.session.query(
                func.count(Visit.id).label('total'),
                cast(Visit.datetime, Date).label('date')
            ).filter(
               Visit.datetime.between(start, end)
            ).group_by('date').order_by(asc('date'))

    @staticmethod
    def total_by_year_month(year: int, month=None):
        if year < 2020:
            raise Exception('Ano deve ser maior de 2020')

        if month is None:
            return db.session.query(
                func.count(Visit.id).label('total'),
                cast(Visit.datetime, Date).label('date')
            ).filter(
                extract('year', Visit.datetime) == year
            ).group_by('date')
        if month < 1 or month > 12:
            raise Exception('Mês inválido')
       
        return db.session.query(
            func.count(Visit.id).label('total'),
            cast(Visit.datetime, Date).label('date')
        ).filter(
            extract('year', Visit.datetime) == year,
            extract('month', Visit.datetime) == month
        ).group_by('date')
    @staticmethod
    def visits_by_ip(ips : list = None):
        """Return a query object with a lista of network in ips and the count of access

        Args:
            ips (list, optional): IPs. Defaults to None.

        Returns:
            BaseQuery: A BaseQuery with number of access for each IP
        """        
        if list is None:
            query = db.session.query(Network, func.count(Network.id).label('views')).join(Visit.network).group_by(Network)
        else:
            query = db.session.query(Network, func.count(Network.id).label('views')).join(Visit.network).filter(Network.ip.in_(ips)).group_by(Network)
        return query