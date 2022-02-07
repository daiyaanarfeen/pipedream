import json
import sys
sys.path.append("..")
import graph
try:
    A = json.load(open('A.json', 'r'))
    compute_times = json.load(open('compute_times.json', 'r'))
    for i in range(len(compute_times)):
        for j in range(len(compute_times[0])):
            compute_times[i][j] = compute_times[i][j][-1][0]
    parameter_sizes = json.load(open('parameter_sizes.json', 'r'))
except:
    pass

gr = graph.Graph.from_str(open('gnmt_partitioned/gpus=12.txt', 'r').read())
stage2nodes = {}
for i in range(12):
    nodes = []
    for k, v in gr.nodes.items():
            if v.stage_id == i:
                    nodes.append((k, v))
    stage2nodes[i] = nodes

def compute_time(k, j, speed, m_prime=1, bandwidth=3125000000.0):
    last_stage_time = compute_times[k+1][j]
    last_stage_parameter_size = parameter_sizes[k+1][j]
    last_stage_time = sum([last_stage_time,
    ((4 * (m_prime - 1) *
        last_stage_parameter_size) / (bandwidth * m_prime))])   
    last_stage_time /= m_prime
    last_stage_time /= speed
    return last_stage_time
