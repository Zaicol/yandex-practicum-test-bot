from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_url = 'sqlite:///yp_tb.db'
engine = create_engine(db_url)
engine.connect()
Base = declarative_base()


class Media(Base):
    __tablename__ = 'media'
    id = Column('id', Integer(), primary_key=True)
    name = Column('name', String(100))
    type = Column('type', String(20), default='image')
    data = Column('data', String(300))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
