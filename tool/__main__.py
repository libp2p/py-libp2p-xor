import argparse

import lookup


def show_lookup(args):
    lookup_log_filename = args.filename
    id = args.id
    events = lookup.filter_lookup(lookup.load_file(lookup_log_filename), id)
    model = lookup.lookup_from_events(events)
    lookup.plot_lookup(model)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command_name', help='sub-command help')

    # parser for show lookup
    parser_show_lookup = subparsers.add_parser("showlookup", help="Visualize a lookup.")
    parser_show_lookup.add_argument("--id", metavar="id", help="Lookup ID", required=True)
    parser_show_lookup.add_argument("filename", help="Lookup log file name")
    parser_show_lookup.set_defaults(handler=show_lookup)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    args.handler(args)
