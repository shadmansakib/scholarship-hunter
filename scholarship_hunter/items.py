# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import calendar
import re
from datetime import date

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Compose


def validate_date(date_str):
    # TODO: This is a quick and dirty fix. Reformat later
    """
    possible formats
    - 15 March 2020
    - 15 November
    - October 31, 2020
    - June 2020
    - September, 2020
    - July 24th
    -


15 March 2020
15 November
October 31, 2020
June 2020
September, 2020
July 24th

    :param date_str:
    :return:
    """
    month_values = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
    }

    # October 31, 2020 or October 1 2020 format
    month_date_year = re.search('^([a-zA-Z]+) (\d{1,2}),* (\d{0,4})$', date_str)
    if month_date_year:
        month = month_date_year.group(1)
        month = month_values[month]
        day = month_date_year.group(2)
        day = int(day)
        year = month_date_year.group(3)
        year = int(year)

        return date(year, month, day)

    # 15 March 2020 or 15 March, 2020 or 15 November format
    date_month_year = re.search('^(\d{1,2}) ([a-zA-Z]+),*\s*(\d{0,4})$', date_str)
    if date_month_year:
        day = int(date_month_year.group(1))
        month = month_values[date_month_year.group(2)]
        try:
            year = int(date_month_year.group(3))
        except Exception as e:
            print(">>> [ERROR] Year not found : {}".format(e))
            year = date.today().year

        return date(year, month, day)

    # June 2020 or September, 2020 or July 24th or October 1
    month_yr_dt = re.search('^([a-zA-Z]+),*\s*(\d{0,4})[a-z]*$', date_str)
    if month_yr_dt:
        month = month_values[month_yr_dt.group(1)]
        if len(month_yr_dt.group(2)) > 2:
            year = int(month_yr_dt.group((2)))
            # set day to last possible date of current month
            day = calendar.monthrange(year, month)[1]
        elif len(month_yr_dt.group(2)) < 2:
            day = int(month_yr_dt.group((2)))
            year = date.today().year
        return date(year, month, day)
    return None


class ScholarshipLoader(ItemLoader):
    default_output_processor = TakeFirst()

    title_in = MapCompose(lambda item: item.replace('\n', '').replace('\t', '').strip())
    university_in = MapCompose(Join(separator=''), lambda item: re.sub('^[a-zA-Z\s]*:','', item).strip())
    deadline_in = MapCompose(lambda item: item.replace(':', '').strip(), validate_date)
    department_in = MapCompose(lambda item: re.sub('[":/]+', '', item).strip())
    course_level_in = MapCompose(Join(separator=''), lambda item: re.sub('^[Course]*[elvL\s:]+', '', item).strip())
    awards_in = MapCompose(lambda item: item.replace('"', '').replace(':', '').strip())

    nationality_in = MapCompose(lambda item: item.replace('"', '').replace(':', '').strip())
    nationality_out = Compose(Join(), lambda item: item.replace('Nationality', '').strip())


class Scholarship(scrapy.Item):
    title = scrapy.Field()
    deadline = scrapy.Field()
    university = scrapy.Field()
    department = scrapy.Field()
    course_level = scrapy.Field()
    awards = scrapy.Field()
    nationality = scrapy.Field()
    application_url = scrapy.Field()
    source_url = scrapy.Field()
