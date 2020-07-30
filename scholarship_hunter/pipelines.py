# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import sessionmaker

from scholarship_hunter.db.sql import db_connect, create_tables
from scholarship_hunter.db.models import Scholarship


class ValidateScholarship:
    """
    Removes scraped contents that are not actually scholarship but other article
    """

    def process_item(self, item, spider):
        # TODO: Drop invalid scholarship
        if not item.get("university") or not item.get("department") or not item.get("application_url"):
            raise DropItem(">>> '' is not a valid scholarship".format(item.get("title")))
        return item


class DropDuplicateScholarship:
    """
    Removes scholarship that already exists
    """

    def process_item(self, scholarship, spider):
        return scholarship


class SaveScholarship:
    def __init__(self):
        # connect to db
        db_engine = db_connect(get_project_settings()["SQL_CONNECTION_STRING"])
        # create tables if not exists
        create_tables(db_engine)

        # session
        # TODO: move to open_spider() function ?
        self.Session = sessionmaker(bind=db_engine)

    def process_item(self, scholarship_item, spider):
        # init db session
        session = self.Session()

        # model instance
        # TODO: automate using for loop
        scholarship = Scholarship()
        scholarship.title = scholarship_item.get('title')
        scholarship.university = scholarship_item.get('university')
        scholarship.department = scholarship_item.get('department')
        scholarship.course_level = scholarship_item.get('course_level')
        scholarship.deadline = scholarship_item.get('deadline')    # works
        scholarship.awards = scholarship_item.get('awards')
        scholarship.nationality = scholarship_item.get('nationality')
        scholarship.application_url = scholarship_item.get('application_url')
        scholarship.data_source = scholarship_item.get('source_url')

        # TODO: move this check to ValidateScholarship pipeline
        # check if data already exists in db, only get the 'title' field of scholarship
        scholarship_exists = session.query(Scholarship, Scholarship.title).filter(
            Scholarship.application_url == scholarship.application_url).first()
        if scholarship_exists:
            raise DropItem(">>> [EXISTS] Scholarship '{}' already exists in db".format(scholarship.title))

        try:
            session.add(scholarship)
            session.commit()
            print(">>> [SAVED] Scholarship saved")

        except Exception as e:
            print('>>> [ERROR] Cannot commit database session :: {}'.format(e))

        return scholarship_item
