import argparse

import lookup


def show_lookup(args):
    events = lookup.filter_lookup(lookup.load_file(args.filename), args.id)
    model = lookup.lookup_from_events(events, args.zoom)
    lookup.plot_lookup(model)


def expected_fill(args):
    events = lookup.load_file(args.filename)  # all events across all lookups
    fill = lookup.compute_expected_fill(events)
    for j in range(len(fill)):
        print("Bucket {}: expected_fill={}".format(j + 1, fill[j]))


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command_name', help='sub-command help')

    # parser for show lookup
    parser_show_lookup = subparsers.add_parser("showlookup", help="Visualize a lookup.")
    parser_show_lookup.add_argument("--id", metavar="id", help="Lookup ID", required=True)
    parser_show_lookup.add_argument("--zoom", metavar="zoom", help="Zoom level.", default=4.0)
    parser_show_lookup.add_argument("filename", help="Lookup log file name")
    parser_show_lookup.set_defaults(handler=show_lookup)

    # parser for expected routing table fill
    parser_show_lookup = subparsers.add_parser("expectedfill", help="Report expected routing table fill, based on lookup history.")
    parser_show_lookup.add_argument("filename", help="Lookup log file name")
    parser_show_lookup.set_defaults(handler=expected_fill)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    args.handler(args)
