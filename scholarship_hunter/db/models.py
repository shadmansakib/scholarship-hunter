
# See: https://overiq.com/sqlalchemy-101/defining-schema-in-sqlalchemy-orm/


from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date
from scholarship_hunter.db.sql import Base


class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    # TODO: 1-2-m
    university = Column(String)
    deadline = Column(Date)    # experimental
    # TODO: 1-2-m
    department = Column(String)
    # TODO: m2m
    course_level = Column(String)
    awards = Column(String)
    # TODO: m2m
    nationality = Column(String)
    application_url = Column(String, unique=True)
    data_source = Column(String, unique=True)

    created_on = Column(DateTime(), default=datetime.now)
