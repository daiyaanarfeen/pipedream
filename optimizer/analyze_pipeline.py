import sys
sys.path.append('..')
import graph
gr = graph.Graph.from_str(open('./gnmt/gpus=12.txt', 'r').read())
stage2nodes = {}
for i in range(12):
    nodes = []
    for k, v in gr.nodes.items():
            if v.stage_id == i:
                    nodes.append((k, v))
    stage2nodes[i] = nodes