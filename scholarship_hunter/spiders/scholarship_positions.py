from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scholarship_hunter.items import Scholarship, ScholarshipLoader


class ScholarshipPositions(CrawlSpider):
    name = 'scholarship_positions'
    allowed_domains = ['scholarship-positions.com',]
    start_urls = [
        'https://scholarship-positions.com/category/masters-scholarships/',
        'https://scholarship-positions.com/category/under-graduate-scholarship/',
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=r'[a-z\-]*/\d{4}/\d{2}/\d{2}/',
                unique=True
            ),
            callback='parse_scholarship',
        ),

        # follow next page
        Rule(
            LinkExtractor(
                # restrict_xpaths='//div[@class="nav-next"]/a[contains(text(), "Older posts")]/@href',
                allow=r'/page/[0-9]+',
            ),
            follow=True,

        ),
    )

    def parse_scholarship(self, response):
        # itemloader
        loader = ScholarshipLoader(item=Scholarship(), response=response)

        loader.add_xpath(
            'title',
            '//article/header/h1/text()',
        )

        loader.add_xpath(
            'university',
            '//strong[contains(text(), "University") or contains(text(), "University or Organization")]/parent::li/text()',
        )

        loader.add_xpath(
            'application_url',
            '//a[normalize-space(.) = "Apply Now"]/@href'
        )

        loader.add_xpath(
            'deadline',
            '//strong[contains(text(), "Application Deadline")]/parent::p/text()',
        )

        loader.add_xpath(
            'department',
            '//strong[contains(text(), "Department")]/parent::li/text()',
        )

        loader.add_xpath(
            'course_level',
            # '//strong[contains(text(), "Course Level")]/parent::li//text()',    # *sometimes* doesn't work
            # '//strong[contains(text(), "Course Lev")]/parent::li//text()',    # *sometimes* doesn't work
            '//strong[contains(text(), "urse Lev")]/parent::li//text()',
        )

        loader.add_xpath(
            'awards',
            '//strong[contains(text(), "Award") or contains(text(), "Awards")]/parent::li/text()',

        )

        loader.add_xpath(
            'nationality',
            # '//strong[contains(text(), "Nationality")]/parent::li/text()',    # *sometimes* does not work
            '//strong[contains(text(), "Nationality")]/parent::*/descendant-or-self::*/text()'
        )

        loader.add_value(
            'source_url',
            response.url
        )

        return loader.load_item()
