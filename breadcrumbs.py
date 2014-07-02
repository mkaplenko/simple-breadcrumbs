__author__ = 'mkaplenko'
from flask import render_template, Markup


class BreadCrumbItem(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url


class BreadCrumbs(object):
    def __init__(self):
        self.items = []
        self.iteration_position = 0

    def __call__(self, *args, **kwargs):
        return Markup(render_template('breadcrumbs.html', path=self))

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        return self

    def __contains__(self, item):
        return item in self.items

    def next(self):
        if self.iteration_position >= len(self.items):
            raise StopIteration
        item = self.items[self.iteration_position]
        self.iteration_position += 1
        return item

    def add_item(self, title, url):
        self.items.append(BreadCrumbItem(title, url))
