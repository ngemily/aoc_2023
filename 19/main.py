from dataclasses import dataclass
from functools import partial

import re
import operator
import pudb


@dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int


workflows = [
    "px{a<2006:qkq,m>2090:A,rfg}",
    "pv{a>1716:R,A}",
    "lnx{m>1548:A,A}",
    "rfg{s<537:gd,x>2440:R,A}",
    "qs{s>3448:A,lnx}",
    "qkq{x<1416:A,crn}",
    "crn{x>2662:A,R}",
    "in{s<1351:px,qqz}",
    "qqz{s>2770:qs,m<1801:hdj,R}",
    "gd{a>3333:R,R}",
    "hdj{m>838:A,pv}",
]
parts = [
    "{x=787,m=2655,a=1222,s=2876}",
    "{x=1679,m=44,a=2067,s=496}",
    "{x=2036,m=264,a=79,s=2244}",
    "{x=2461,m=1339,a=466,s=291}",
    "{x=2127,m=1623,a=2188,s=1013}",
]


def parse_workflow(workflow):
    wid, rules = re.match(r"(\w+){(.*)}", workflow).groups()
    rules = rules.split(",")

    def parse_rule(rule):
        condition, dest = rule.split(":")
        attr, cmp, val = (
            condition[0],
            operator.lt if condition[1] == "<" else operator.gt,
            int(condition[2:]),
        )
        # print(condition, attr, cmp, val, dest)
        return (lambda p: cmp(getattr(p, attr), val), dest)

    rules = list(map(parse_rule, rules[:-1])) + [(lambda p: True, rules[-1])]
    return (wid, rules)


def parse_part(part):
    x, m, a, s = part[1:-1].split(",")
    x, m, a, s = int(x[2:]), int(m[2:]), int(a[2:]), int(s[2:])
    return Part(x, m, a, s)


def get_walker(workflows, init):
    def walk(part, it):
        cond, dst = next(it)
        while not cond(part):
            cond, dst = next(it)
        yield dst
        yield from walk(part, iter(workflows[dst]))

    def _(part):
        for step in walk(part, init):
            if step in ["A", "R"]:
                return step == "A"

    return _


def pt_1():
    with open("input.txt") as fh:
        workflows = []
        for line in map(lambda s: s.strip(), fh):
            if line == "":
                break
            workflows.append(line)
        workflows = dict(map(parse_workflow, workflows))
        parts = list(map(parse_part, map(lambda s: s.strip(), fh)))


    f = partial(get_walker, workflows=workflows)
    print(
        sum(
            map(
                lambda part: part.x + part.m + part.a + part.s,
                filter(lambda part: f(init=iter(workflows["in"]))(part), parts),
            )
        )
    )

pt_1()  # 350678
