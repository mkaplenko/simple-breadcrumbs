__author__ = 'mkaplenko'
from math import ceil
from flask import render_template, Markup


class Page(object):
    def __init__(self, number, paginator):
        self.number = number
        self.paginator = paginator

    @property
    def has_next(self):
        return True if self.number < self.paginator.num_pages else False

    @property
    def has_previous(self):
        return True if self.number > 1 and self.paginator.num_pages > 1 else False

    @property
    def has_other_pages(self):
        return False if self.number == 1 and self.paginator.num_pages == 1 else True

    @property
    def previous_page_number(self):
        return self.number - 1 if self.has_previous else None

    @property
    def next_page_number(self):
        return self.number + 1 if self.has_next else None

    @property
    def start_index(self):
        return self.number * self.paginator.paginate_by - self.paginator.paginate_by - 1

    @property
    def end_index(self):
        last_counter = self.number * self.paginator.paginate_by
        return last_counter if last_counter < self.paginator.items_count else self.paginator.items_count


class Paginator(object):
    def __init__(self, **kwargs):
        self.paginate_by = kwargs['paginate_by']
        self.query = kwargs['query']
        self.items_count = self.query.count()
        self.render_template = kwargs.get('render_template', 'pagenav.html')
        self.page_number = self.__validate_page_number(kwargs.get('page', 1))
        self.page = Page(self.page_number, self)

    def __call__(self, *args, **kwargs):
        return Markup(render_template(self.render_template, paginator=self))

    @property
    def items(self):
        return self.query.offset(self.paginate_by * (self.page_number - 1)).limit(self.paginate_by)

    @property
    def page_range(self):
        return [x for x in xrange(1, self.num_pages+1)]

    @property
    def num_pages(self):
        result = int(ceil(self.items_count*1.0/self.paginate_by))
        return result if result > 0 else 1

    def __validate_page_number(self, number):
        try:
            number = int(int(number) // 1)
        except ValueError:
            number = 1
        number = number if number > 0 else 1
        return number if number < self.num_pages else self.num_pages