input = """Step B must be finished before step X can begin.
Step H must be finished before step P can begin.
Step Y must be finished before step J can begin.
Step Z must be finished before step I can begin.
Step T must be finished before step U can begin.
Step R must be finished before step C can begin.
Step S must be finished before step J can begin.
Step W must be finished before step J can begin.
Step C must be finished before step L can begin.
Step L must be finished before step F can begin.
Step E must be finished before step G can begin.
Step A must be finished before step G can begin.
Step V must be finished before step X can begin.
Step U must be finished before step O can begin.
Step P must be finished before step F can begin.
Step O must be finished before step I can begin.
Step I must be finished before step F can begin.
Step K must be finished before step F can begin.
Step J must be finished before step F can begin.
Step G must be finished before step X can begin.
Step M must be finished before step X can begin.
Step F must be finished before step Q can begin.
Step Q must be finished before step N can begin.
Step D must be finished before step N can begin.
Step X must be finished before step N can begin.
Step I must be finished before step Q can begin.
Step U must be finished before step I can begin.
Step D must be finished before step X can begin.
Step B must be finished before step W can begin.
Step L must be finished before step N can begin.
Step U must be finished before step X can begin.
Step U must be finished before step J can begin.
Step C must be finished before step V can begin.
Step G must be finished before step N can begin.
Step S must be finished before step K can begin.
Step Q must be finished before step D can begin.
Step J must be finished before step X can begin.
Step V must be finished before step K can begin.
Step Z must be finished before step A can begin.
Step L must be finished before step M can begin.
Step H must be finished before step D can begin.
Step V must be finished before step Q can begin.
Step L must be finished before step V can begin.
Step S must be finished before step D can begin.
Step C must be finished before step Q can begin.
Step S must be finished before step L can begin.
Step E must be finished before step V can begin.
Step E must be finished before step P can begin.
Step C must be finished before step I can begin.
Step O must be finished before step K can begin.
Step H must be finished before step V can begin.
Step M must be finished before step F can begin.
Step K must be finished before step N can begin.
Step C must be finished before step X can begin.
Step G must be finished before step D can begin.
Step E must be finished before step U can begin.
Step R must be finished before step L can begin.
Step K must be finished before step G can begin.
Step W must be finished before step C can begin.
Step B must be finished before step L can begin.
Step L must be finished before step J can begin.
Step U must be finished before step D can begin.
Step I must be finished before step G can begin.
Step Q must be finished before step X can begin.
Step B must be finished before step M can begin.
Step T must be finished before step P can begin.
Step G must be finished before step Q can begin.
Step Y must be finished before step U can begin.
Step M must be finished before step D can begin.
Step P must be finished before step I can begin.
Step I must be finished before step K can begin.
Step O must be finished before step M can begin.
Step H must be finished before step Z can begin.
Step V must be finished before step M can begin.
Step P must be finished before step J can begin.
Step B must be finished before step U can begin.
Step E must be finished before step X can begin.
Step M must be finished before step Q can begin.
Step W must be finished before step L can begin.
Step O must be finished before step J can begin.
Step I must be finished before step X can begin.
Step J must be finished before step N can begin.
Step Y must be finished before step S can begin.
Step E must be finished before step D can begin.
Step M must be finished before step N can begin.
Step E must be finished before step O can begin.
Step I must be finished before step D can begin.
Step V must be finished before step N can begin.
Step R must be finished before step X can begin.
Step Z must be finished before step O can begin.
Step O must be finished before step X can begin.
Step I must be finished before step J can begin.
Step S must be finished before step E can begin.
Step E must be finished before step Q can begin.
Step J must be finished before step Q can begin.
Step H must be finished before step Y can begin.
Step T must be finished before step G can begin.
Step S must be finished before step A can begin.
Step P must be finished before step K can begin.
Step A must be finished before step D can begin.
Step B must be finished before step P can begin."""

test_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

import re

class Node:
    def __init__(self, value):
        self.value = value
        self.requirements = set()
    def push_requirement(self, requirement):
        self.requirements.add(requirement)

node_ids = set()
node_registry = {}
node_ids_by_requirement = {}

for i in input.split("\n"):
    match = re.match('.* ([A-Z]) .* ([A-Z]) .*', i)
    required_step = match.group(1)
    step = match.group(2)

    if required_step not in node_registry:
        node_registry[required_step] = Node(required_step)
    if required_step not in node_ids_by_requirement:
        node_ids_by_requirement[required_step] = []
    node_ids_by_requirement[required_step].append(step)

    if step not in node_registry:
        node_registry[step] = Node(step)
    node = node_registry[step]
    node.push_requirement(required_step)

# find root nodes (nodes with no requirements)
root_node_ids = []
for i in node_registry:
    node = node_registry[i]
    if len(node.requirements) == 0:
        root_node_ids.append(node.value)
root_node_ids.sort()

class Worker:
    def __init__(self):
        self.count = 0

    def set_working(self, working):
        self.working = working

    def set_count(self, count):
        self.count = count

    def count_down(self):
        self.count -= 1

    def set_blocked_node_ids(self, node_ids):
        self.blocked_node_ids = node_ids

workers = []
for i in range(0, 5):
    workers.append(Worker())

time = -1
values_in_order = []
node_ids_to_traverse = []
node_ids_to_traverse.extend(root_node_ids)
while len(values_in_order) < len(node_registry):

    time += 1

    # count down workers and choose one
    available_workers = []
    for i, worker in enumerate(workers):
        if worker.count > 0:
            worker.count_down()
            if worker.count == 0:
                values_in_order.append(worker.working)
                node_ids_to_traverse.extend(worker.blocked_node_ids)
                worker.blocked_node_ids = []
                available_workers.append(worker)
        elif worker.count == 0:
            available_workers.append(worker)

    for found_worker in available_workers:
        if len(node_ids_to_traverse) > 0:

            node_id = node_ids_to_traverse.pop(0)
            found_worker.set_working(node_id)
            found_worker.count = ord(node_id) - 64 + 60

            next_node_ids = []

            if node_id in node_ids_by_requirement:
                node_ids_that_require_this = node_ids_by_requirement[node_id]
                for i in node_ids_that_require_this:
                    blocked_node = node_registry[i]
                    blocked_node.requirements.remove(node_id)
                    if len(blocked_node.requirements) == 0:
                        next_node_ids.append(blocked_node.value)
            
            next_node_ids.sort()
            found_worker.set_blocked_node_ids(next_node_ids)

for i in workers:
    time += i.count

print("part 1: " + ''.join(values_in_order))
print("part 2: " + str(time))