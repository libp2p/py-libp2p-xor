import json
from dataclasses import dataclass
from typing import List

from key import *


@dataclass
class StateUpdateEvent:
    cause: Key  # peer that caused this event
    source: Key
    heard: List[Key]
    waiting: List[Key]
    queried: List[Key]
    unreachable: List[Key]

    def contains(self, key):
        if self.cause == key or self.source == key:
            return True
        if key in self.heard:
            return True
        if key in self.waiting:
            return True
        if key in self.queried:
            return True
        if key in self.unreachable:
            return True
        return False


@dataclass
class Event:
    lookup_id: str
    stamp_ns: int
    node: Key  # node performing the lookup
    target: Key  # target of the lookup
    request: StateUpdateEvent
    response: StateUpdateEvent

    def contains(self, key):
        req = self.request.contains(key) if self.request else False
        resp = self.response.contains(key) if self.response else False
        return req or resp

    def heard(self):
        req = self.request.heard if self.request else []
        resp = self.response.heard if self.response else []
        return req + resp

    def waiting(self):
        req = self.request.waiting if self.request else []
        resp = self.response.waiting if self.response else []
        return req + resp

    def queried(self):
        req = self.request.queried if self.request else []
        resp = self.response.queried if self.response else []
        return req + resp

    def unreachable(self):
        req = self.request.unreachable if self.request else []
        resp = self.response.unreachable if self.response else []
        return req + resp

    def requesting_peer(self):
        if self.request and len(self.request.waiting) == 1:
            return self.request.waiting[0]
        else:
            return None

    def responding_peer(self):
        if self.response:
            return self.response.cause
        else:
            return None


def parse_state_update_from_json(data):
    if not data:
        return None
    else:
        return StateUpdateEvent(
            cause=key_from_base64_kbucket_id(data["Cause"]["Kad"]),
            source=key_from_base64_kbucket_id(data["Source"]["Kad"]),
            heard=[key_from_base64_kbucket_id(id["Kad"]) for id in data.get("Heard", [])],
            waiting=[key_from_base64_kbucket_id(id["Kad"]) for id in data.get("Waiting", [])],
            queried=[key_from_base64_kbucket_id(id["Kad"]) for id in data.get("Queried", [])],
            unreachable=[key_from_base64_kbucket_id(id["Kad"]) for id in data.get("Unreachable", [])],
        )


def parse_event_from_json(data):
    info = data["info"]
    return Event(
        lookup_id=info["ID"],
        stamp_ns=data["ts"],
        node=key_from_base64_kbucket_id(info["Node"]["Kad"]),
        target=key_from_base64_kbucket_id(info["Key"]["Kad"]),
        request=parse_state_update_from_json(info.get("Request")),
        response=parse_state_update_from_json(info.get("Response")),
    )


def load_file(filename: str):
    events = []
    with open(filename) as f:
        for line in f:
            data = json.loads(line)
            events.append(parse_event_from_json(data))
    return events


def filter_lookup(events: List[Event], lookup_id: str):
    return [ev for ev in events if ev.lookup_id == lookup_id]


def group_events_into_lookups(events: List[Event]):
    lkp = {}  # lookup_id -> ordered list of lookup events
    for e in events:
        g = lkp.get(e.lookup_id)
        if not g:
            g = []
            lkp[e.lookup_id] = g
        g.append(e)
    return lkp
