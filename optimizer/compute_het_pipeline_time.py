import json
import sys
sys.path.append("..")
import graph
try:
    A = json.load(open('A.json', 'r'))
    compute_times = json.load(open('compute_times.json', 'r'))
    parameter_sizes = json.load(open('parameter_sizes.json', 'r'))
    activation_sizes = json.load(open('activation_sizes.json', 'r')) 
except:
    pass

gr = graph.Graph.from_str(open('gnmt/gpus=12.txt', 'r').read())
stage2nodes = {}
for i in range(12):
    nodes = []
    for k, v in gr.nodes.items():
            if v.stage_id == i:
                    nodes.append((k, v))
    stage2nodes[i] = nodes

cur_end = len(A) - 2
super_stage_splits = [cur_end]
cur_machines_left = len(A[0][cur_end]) - 1
while True:
    if A[0][cur_end][cur_machines_left][1] is None:
        break
    cur_end = A[0][cur_end][cur_machines_left][1][0]
    super_stage_splits.insert(0, cur_end)
    cur_machines_left = A[0][cur_end][cur_machines_left][1][1] 
super_stage_splits.insert(0, 0)

sub_stage_splits = []
for i in range(len(super_stage_splits)-1):
    beg = super_stage_splits[i]
    cur_end = super_stage_splits[i+1] 
    cur_stage_splits = [cur_end]
    cur_machines_left = len(compute_times[beg][cur_end]) - 1
    while True:
        if compute_times[beg][cur_end][cur_machines_left][1] is None:
            break
        cur_end = compute_times[beg][cur_end][cur_machines_left][1][0]
        cur_stage_splits.insert(0, cur_end)
        cur_machines_left = compute_times[beg][cur_end][cur_machines_left][1][1]
    cur_stage_splits.insert(0, beg)
    sub_stage_splits.append(cur_stage_splits)