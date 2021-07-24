from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import base
from sqlalchemy.sql.expression import true
from sqlalchemy.types import Date
from sqlalchemy.util.compat import dataclass_fields
from .DataBase import Base

class Record(base) :
    _tablename_ = "Records"


    id = Column(Integer, primary_key=True, index=true)
    date = Column(Date)
    country = Column(String(255), index=True)
    cases = Column(Integer)
    deaths = Column(Integer)
    recoveries = Column(Integer)