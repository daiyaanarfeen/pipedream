import argparse
import pickle
import sys
sys.path.append("..")
import graph

parser = argparse.ArgumentParser()
parser.add_argument('dir', type=str)
parser.add_argument('num_gpus', type=int)
parser.add_argument('bw', type=float, nargs='+')
args = parser.parse_args()

all_As = pickle.load(open('%s/all_As.pkl'%args.dir, 'rb'))
compute_times, A = all_As
parameter_sizes = pickle.load(open('%s/param_sizes.pkl'%args.dir, 'rb'))
activation_sizes = pickle.load(open('%s/act_sizes.pkl'%args.dir, 'rb')) 
antichain_nodes = pickle.load(open('%s/antichain_nodes.pkl'%args.dir, 'rb'))

gr = graph.Graph.from_str(open('%s/gpus=%d.txt'%(args.dir, args.num_gpus), 'r').read())
stage2nodes = {}
for i in range(args.num_gpus):
    nodes = []
    for k, v in gr.nodes.items():
            if v.stage_id == i:
                    nodes.append((k, v))
    stage2nodes[i] = nodes

predecessors = []
for antichain_node in antichain_nodes:
    antichain_node = antichain_node.antichain
    predecessors.append(gr.all_predecessors(antichain_node))


cur_end = len(A) - 2
super_stage_splits = [cur_end+1]
cur_machines_left = len(A[0][cur_end]) - 1
while True:
    if A[0][cur_end][cur_machines_left][1] is None:
        break
    cur_end, cur_machines_left = A[0][cur_end][cur_machines_left][1]
    super_stage_splits.insert(0, cur_end+1)
super_stage_splits.insert(0, 0)

def print_pipeline(super_stage_splits):
    sub_stage_splits = []
    for i in range(len(super_stage_splits)-1):
        beg = super_stage_splits[i]
        cur_end = super_stage_splits[i+1] - 1
        cur_stage_splits = [cur_end+1]
        cur_machines_left = len(compute_times[beg][cur_end]) - 1
        while True:
            if compute_times[beg][cur_end][cur_machines_left][1] is None:
                break
            cur_end, cur_machines_left = compute_times[beg][cur_end][cur_machines_left][1]
            cur_stage_splits.insert(0, cur_end+1)
        cur_stage_splits.insert(0, beg)
        sub_stage_splits.append(cur_stage_splits)
    
    for i in range(len(super_stage_splits)-1):
        print(compute_times[super_stage_splits[i]][super_stage_splits[i+1]-1][-1])
        
        for j in range(len(sub_stage_splits[i])-1):
            print('\t', compute_times[sub_stage_splits[i][j]][sub_stage_splits[i][j+1]-1][0])
            if j != len(sub_stage_splits[i]) - 2:
                print('\t', '| %f'%(2.0 * activation_sizes[sub_stage_splits[i][j+1]-1] / args.bw[0]))
                print('\t', 'v')
    
        if i != len(super_stage_splits) - 2:
            print('| %f'%(2.0 * activation_sizes[super_stage_splits[i+1]-1] / args.bw[1]))
            print('v')

import numpy as np
multiplier = np.array([1, 1, 1, 1])
times = [max(np.array([compute_times[0][i][-1][0], compute_times[i+1][j][-1][0], compute_times[j+1][k][-1][0], compute_times[k+1][98][-1][0]]) / multiplier) \
    for k in range(99) for j in range(k) for i in range(j) \
    if compute_times[0][i][-1][0] is not None and compute_times[i+1][j][-1][0] is not None and compute_times[j+1][k][-1][0] is not None and compute_times[k+1][98][-1][0] is not None] 
splits = [(0, i+1, j+1, k+1, 99) for k in range(99) for j in range(k) for i in range(j) \
    if compute_times[0][i][-1][0] is not None and compute_times[i+1][j][-1][0] is not None and compute_times[j+1][k][-1][0] is not None and compute_times[k+1][98][-1][0] is not None]

multiplier = np.array([1, 1, 2])
times = [max(np.array([compute_times[0][i][-1][0], compute_times[i+1][j][-1][0], compute_times[j+1][98][-1][0]]) / multiplier) \
    for j in range(99) for i in range(j) \
    if compute_times[0][i][-1][0] is not None and compute_times[i+1][j][-1][0] is not None and compute_times[j+1][98][-1][0] is not None] 
splits = [(0, i+1, j+1, 99) for j in range(99) for i in range(j) \
    if compute_times[0][i][-1][0] is not None and compute_times[i+1][j][-1][0] is not None and compute_times[j+1][98][-1][0] is not None]