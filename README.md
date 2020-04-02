# py-libp2p-xor

## Summary

This repo will grow into a collection of Python libraries for XOR arithmetic, as well as
apps for analyzing and visualizing Kademlia DHT routing logs.

### Show lookup

The "show lookup" command-line tool visualizes a lookup execution. To invoke it,
from the root directory of this repo, run:

    python -m tool showlookup --id=LOOKUP_ID DHT_LOOKUPS_LOG_FILENAME

You should see something like:

![Lookup visualization](https://raw.githubusercontent.com/libp2p/py-libp2p-xor/master/assets/lookup_sample.png)

How to read this:

* The X-axis represents time, measured in milliseconds since the start of the lookup
* The Y-axis represents peers by their distance to the lookup target. The left Y-axis shows distance to target, while
the right Y-axis shows peer XOR keys
* _Grey horizontal grid lines_ indicate the peers that were encountered throughout the lookup
* _Grey vertical grid lines_ indicate lookup events
* _Thick horizontal lines_ represent queries:
    * _Green_ queries are successful. When a query succeeds, the peers it delivers are represented as _small grey discs_ along the vertical grid line, corresponding to the query's end.
    * _Red_ queries are unsuccessful
    * _Blue_ queries did not complete and were aborted by the lookup's termination
    * _Solid green_ queries are successful queries that form a start-to-finish lookup path

## Contribute

Contributions welcome. Please check out [the issues](https://github.com/libp2p/go-libp2p-xor/issues).

Check out our [contributing document](https://github.com/libp2p/community/blob/master/CONTRIBUTE.md) for more information on how we work, and about contributing in general. Please be aware that all interactions related to libp2p are subject to the IPFS [Code of Conduct](https://github.com/ipfs/community/blob/master/code-of-conduct.md).

## License

[MIT](LICENSE) © Protocol Labs Inc.
