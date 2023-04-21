from setting import ENGINE, Base  
from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.dialects.mysql import TINYINT as Tinyint
from sqlalchemy.dialects.mysql import DOUBLE as Double
  
  
class Inputs(Base):  
    __tablename__ = 'inputs'  
    date   = Column('date', Date, primary_key=True)
    height = Column('height', Integer, primary_key=True, index=True)
    h      = Column('hash', String(64), primary_key=True, index=True)
    addr   = Column('address', String(64), primary_key=True, index=True)
    v      = Column('v', Double) 
    w      = Column('w', String(64))

    def __init__(self, x):
       self.date = x['date']
       self.height = x['height']
       self.h = x['h']
       self.addr = x['addr']
       self.v = x['v']
       self.w = x['w']


if '__main__' == __name__:
    Base.metadata.create_all(ENGINE)
  
