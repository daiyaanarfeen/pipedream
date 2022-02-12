import pickle
import sys
sys.path.append("..")
import graph

all_As = pickle.load(open('gnmt/all_As.pkl', 'rb'))
compute_times, A = all_As
parameter_sizes = pickle.load(open('gnmt/param_sizes.pkl', 'rb'))
activation_sizes = pickle.load(open('gnmt/act_sizes.pkl', 'rb')) 
antichain_nodes = pickle.load(open('gnmt/antichain_nodes.pkl', 'rb'))

gr = graph.Graph.from_str(open('gnmt/gpus=12.txt', 'r').read())
stage2nodes = {}
for i in range(12):
    nodes = []
    for k, v in gr.nodes.items():
            if v.stage_id == i:
                    nodes.append((k, v))
    stage2nodes[i] = nodes

cur_end = len(A) - 2
super_stage_splits = [cur_end+1]
cur_machines_left = len(A[0][cur_end]) - 1
while True:
    if A[0][cur_end][cur_machines_left][1] is None:
        break
    cur_end = A[0][cur_end][cur_machines_left][1][0]
    super_stage_splits.insert(0, cur_end+1)
    cur_machines_left = A[0][cur_end][cur_machines_left][1][1] 
super_stage_splits.insert(0, 0)

sub_stage_splits = []
for i in range(len(super_stage_splits)-1):
    beg = super_stage_splits[i]
    cur_end = super_stage_splits[i+1] - 1
    cur_stage_splits = [cur_end+1]
    cur_machines_left = len(compute_times[beg][cur_end]) - 1
    while True:
        if compute_times[beg][cur_end][cur_machines_left][1] is None:
            break
        cur_end = compute_times[beg][cur_end][cur_machines_left][1][0]
        cur_stage_splits.insert(0, cur_end+1)
        cur_machines_left = compute_times[beg][cur_end][cur_machines_left][1][1]
    cur_stage_splits.insert(0, beg)
    sub_stage_splits.append(cur_stage_splits)

for i in range(len(super_stage_splits)-1):
    print(compute_times[super_stage_splits[i]][super_stage_splits[i+1]-1][-1])
    
    for j in range(len(sub_stage_splits[i])-1):
        print('\t', compute_times[sub_stage_splits[i][j]][sub_stage_splits[i][j+1]-1][0])
        if j != len(sub_stage_splits[i]) - 2:
            print('\t', '| %f'%(2.0 * activation_sizes[sub_stage_splits[i][j+1]-1] / 16e9))
            print('\t', 'v')

    if i != len(super_stage_splits) - 2:
        print('| %f'%(2.0 * activation_sizes[super_stage_splits[i+1]-1] / 3.125e9))
        print('v')

predecessors = []
for antichain_node in antichain_nodes:
    antichain_node = antichain_node.antichain
    predecessors.append(gr.all_predecessors(antichain_node))