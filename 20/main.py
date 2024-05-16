from dataclasses import dataclass
from collections import deque
from enum import StrEnum

import networkx as nx

# 8 low pulses and 4 high pulses per button press
ss = [
    "broadcaster -> a, b, c",
    "%a -> b",
    "%b -> c",
    "%c -> inv",
    "&inv -> a",
]
ss = [
    "broadcaster -> a",
    "%a -> inv, con",
    "&inv -> b",
    "%b -> con",
    "&con -> output",
]


class NodeType(StrEnum):
    FLOP = "%"
    CONJ = "&"
    BROADCASTER = "b"


@dataclass
class Node:
    _id: str
    _type: NodeType
    state: bool | None = False


G = nx.DiGraph()
n = dict()  # node_id to Node object
n["output"] = Node(_id="output", _type=NodeType.BROADCASTER)
n["rx"] = Node(_id="rx", _type=NodeType.BROADCASTER)

with open("input.txt") as fh:
    for line in map(str.strip, fh):
        src, dsts = map(str.strip, line.split("->"))
        dsts = list(map(str.strip, dsts.split(",")))

        src_id = src if src == "broadcaster" else src[1:]
        n[src_id] = Node(_id=src_id, _type=NodeType(src[0]))
        for dst in dsts:
            G.add_edge(src_id, dst)

flops = list(
    filter(
        lambda node: node._type == NodeType.FLOP,
        map(lambda node_id: n[node_id], G.nodes),
    )
)


def get_pulse_counter():
    lo = 0
    hi = 0

    def pulse_counter(pulse):
        nonlocal lo
        nonlocal hi
        if pulse == True:
            hi = hi + 1
        elif pulse == False:
            lo = lo + 1
        return (lo, hi)

    return pulse_counter


def counted(f, counter):
    def _(*args, **kwargs):
        _, pulse = args
        counter(pulse)
        return f(*args, **kwargs)

    return _


def process_pulse(node_id, pulse):
    """Process incoming pulse at node, yielding any outgoing pulses"""
    node = n[node_id]
    if node._type == NodeType.BROADCASTER:
        for dst in G[node._id]:
            yield (dst, pulse)
    if node._type == NodeType.FLOP and not pulse:
        node.state = not node.state
        for dst in G[node._id]:
            yield (dst, node.state)
    elif node._type == NodeType.CONJ:
        srcs = list(map(lambda _id: n[_id], G.predecessors(node._id)))
        node.state = not all(map(lambda node: node.state, srcs))
        for dst in G[node._id]:
            yield (dst, node.state)


def count(f):
    def _(*args, **kwargs):
        pc = get_pulse_counter()
        f(*args, **kwargs, pc=pc)
        return pc(None)

    return _


def broadcast_pulse(elem, pulse, pc):
    """Propagate pulse throughout the circuit"""
    q = deque()
    q.append((elem, pulse))

    while len(q) > 0:
        dst, pulse = q.popleft()
        for dst, pulse in counted(process_pulse, pc)(dst, pulse):
            q.append((dst, pulse))


def pt_1():
    N = 1000
    num_lo, num_hi = 0, 0
    for i in range(N):
        lo, hi = count(broadcast_pulse)("broadcaster", False)
        num_lo, num_hi = num_lo + lo, num_hi + hi

    print(num_lo, num_hi)
    return num_lo * num_hi


print(pt_1())  # 788848550
