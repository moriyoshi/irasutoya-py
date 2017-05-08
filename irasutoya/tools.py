from __future__ import print_function
import sys
import argparse
from .scraper import Scraper


class ApplicationError(Exception):
    @property
    def message(self):
        return self.args[0]


class Subcommand(object):
    def __call__(self):
        pass

    def build_parser(self, parser):
        pass


class CategoriesCommand(Subcommand):
    name = 'categories'

    def __call__(self, scraper, args):
        categories = scraper.fetch_categories()
        for k, v in categories.items():
            print(k)

class ItemsCommand(Subcommand):
    name = 'items'

    def __call__(self, scraper, args):
        category = args.category
        categories = scraper.fetch_categories()
        try:
            search_page_url_for_category = categories[category]
        except KeyError:
            raise ApplicationError('no such category: {}'.format(category))
        with_details = args.with_details
        items = scraper.fetch_all_items_starting_from(search_page_url_for_category, with_details=with_details)
        def _():
            for item in items:
                records = [item[u'title'], item[u'url']]
                if with_details:
                    records.extend([item['description']])
                    for image in item['images']:
                        _records = list(records)
                        _records.extend([image['title'] or u'', image['url']])
                        yield _records
                else:
                    yield records
        for cols in _():
            print(u'\t'.join(cols))

    def build_parser(self, parser):
        parser.add_argument('--with-details', '-d', action='store_true')
        parser.add_argument('category')


subcommands = [
    CategoriesCommand(),
    ItemsCommand(),
    ]

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', title='subcommands')
    command_map = {}
    for subcommand in subcommands:
        subparser = subparsers.add_parser(subcommand.name)
        subcommand.build_parser(subparser)
        command_map[subcommand.name] = subcommand
    args = parser.parse_args()
    scraper = Scraper()
    try:
        command_map[args.command](scraper, args)
    except ApplicationError as e:
        print("{}: {}".format(parser.prog, e.message), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
