import argparse
import matplotlib.pyplot as plt
import lookup
import glob


def show_lookup(args):
    events = lookup.filter_lookup(lookup.load_file(args.filename), args.id)
    model = lookup.lookup_from_events(events, args.zoom)
    lookup.plot_lookup(model)


def expected_fill(args):
    events = lookup.load_file(args.filename)  # all events across all lookups
    report = lookup.compute_expected_fill(events)
    # TODO: print # of events and # of lookups considered
    print("total not unreachable peers", report.num_not_unreachable)
    print("total unreachable peers", report.num_unreachable)
    for j in range(len(report.bucket_fill)):
        print("bucket {} has expected bucket fill={}".format(j + 1, report.bucket_fill[j]))


def lookup_latency(args):
    files = glob.glob(args.fileglob)
    events = []
    for filepath in files:
        file_events = lookup.load_file(filepath)
        for e in file_events:
            e.lookup_id = filepath + ":" + e.lookup_id
        events.extend(file_events)
    latencies = []
    lookups = lookup.group_events_into_lookups(events)
    for l in lookups:
        m = lookup.lookup_from_events(lookups[l], 1.0)
        latencies.append((m.id, m.latency()))
    print("found {} lookups".format(len(latencies)))
    # plot histo
    fig, axs = plt.subplots(1)
    axs.hist([l[1] for l in latencies])
    plt.show()
    # list in ascending order of latency
    latencies.sort(key=lambda l: l[1])
    for l in latencies:
        print("{} has latency {}".format(l[0], l[1]))


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

    # parser for lookup latency
    parser_show_lookup = subparsers.add_parser("lookuplatency", help="Report the distribution of lookup latencies.")
    parser_show_lookup.add_argument("fileglob", help="Glob for lookup log file names")
    parser_show_lookup.set_defaults(handler=lookup_latency)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    args.handler(args)
