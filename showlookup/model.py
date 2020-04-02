from dataclasses import dataclass
from typing import List

from .events import *
from .xor import *


@dataclass
class QueryModel:
    peer: Key  # peer being queried
    request: Event  # query request event
    response: Event  # query response event
    outcome: str  # success, unreachable, unfinished


QUERY_SUCCESS = "success"
QUERY_UNREACHABLE = "unreachable"
QUERY_UNFINISHED = "unfinished"


@dataclass
class LookupModel:
    id: str
    start_ns: int
    stop_ns: int
    node: Key
    target: Key
    used: List[Key]  # used is a dict of all keys of peers that were attempted during the lookup
    queries: List[QueryModel]
    events: List[Event]

    def stamp_to_x(self, stamp_ns: int):
        """Return the x-axis value for a given nanosecond timestamp."""
        # return milliseconds since the first event in the lookup
        return (stamp_ns - self.start_ns) / 1000000.0

    def min_x(self):
        return 0.0

    def max_x(self):
        return (self.stop_ns - self.start_ns) / 1000000.0

    def key_to_y(self, key: Key):
        """Return the y-axis value for a given key."""
        return xor_key(self.target, key).to_float()

    def min_y(self):
        return 0.0

    def max_y(self):
        return 1.0

    def event_key_xy(self, event, key):
        return self.stamp_to_x(event.stamp_ns), self.key_to_y(key)

    def find_closest_success_query(self):
        closest = None
        for q in self.queries:
            if q.outcome == QUERY_SUCCESS:
                if not closest or self.key_to_y(q.peer) < self.key_to_y(closest.peer):
                    closest = q
        return closest

    def find_source_query(self, query):
        """Returns the earliest query that provided the peer in the argument query."""
        sources = []
        for q in self.queries:
            if q.response and q.peer != self.node and q.response.stamp_ns <= query.request.stamp_ns:
                if query.peer in q.response.heard():
                    sources.append(q)
        if len(sources) == 0:
            return None
        else:
            sources.sort(key=lambda q: q.response.stamp_ns)
            return sources[0]

    def find_path(self):
        path = []
        next = self.find_closest_success_query()
        while next:
            path.append(next)
            next = self.find_source_query(next)
        return path


def request_events(events):
    return [e for e in events if e.request]


def response_events(events):
    return [e for e in events if e.response]


def request_matches_response(req, resp):
    peer = req.requesting_peer()
    return peer and resp.responding_peer() == peer


def find_matching_response_event(events, req):
    for resp in response_events(events):
        if request_matches_response(req, resp):
            return resp
    return None


def queries_from_events(events):
    queries = []
    for req in request_events(events):
        resp = find_matching_response_event(events, req)
        if resp:
            queries.append(
                QueryModel(
                    peer=req.requesting_peer(),
                    request=req,
                    response=resp,
                    outcome=QUERY_SUCCESS if len(resp.response.unreachable) == 0 else QUERY_UNREACHABLE,
                )
            )
        else:
            queries.append(
                QueryModel(
                    peer=req.requesting_peer(),
                    request=req,
                    response=None,
                    outcome=QUERY_UNFINISHED,
                )
            )
    return queries


def lookup_from_events(events):
    if len(events) < 2:
        raise Exception("Not enough events to plot")
    # TODO: verify all events same node and target

    did = {}
    used = []

    def push(x):
        if not x:
            return
        if not did.get(x):
            did[x] = True
            used.append(x)

    for e in events:
        [push(k) for k in e.heard()]
        if e.request:
            push(e.request.cause)
            push(e.request.source)
        if e.response:
            push(e.response.cause)
            push(e.response.source)

    return LookupModel(
        id=events[0].lookup_id,
        start_ns=events[0].stamp_ns,
        stop_ns=events[-1].stamp_ns,
        node=events[0].node,
        target=events[0].target,
        used=used,
        queries=queries_from_events(events),
        events=events,
    )
