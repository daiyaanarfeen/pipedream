# PipeDream: Pipeline Parallelism for DNN Training

This repository contains the source code implementation of the following
papers:
- "[PipeDream: Generalized Pipeline Parallelism for DNN Training](https://www.microsoft.com/en-us/research/publication/pipedream-generalized-pipeline-parallelism-for-dnn-training/)",
  which appeared at SOSP 2019 (`pipedream` branch).
- "[Memory-Efficient Pipeline-Parallel DNN Training](https://www.microsoft.com/en-us/research/publication/memory-efficient-pipeline-parallel-dnn-training/)",
  which appeared at ICML 2021 (`pipedream_2bw` branch).

This work was one as part of Microsoft Research's
[Project Fiddle](https://aka.ms/msr-fiddle). This source code is available
under the [MIT License](LICENSE.txt).

# PipeDream-2BW (built on top of Megatron)

This branch contains an implementation of PipeDream-2BW and other model parallelism
baselines (with and without pipelining) built on top of the Megatron codebase
from Nvidia (under the `megatron` sub-directory).

Experiments can be run on AWS using the scripts available in the `scripts/`
sub-directory. Data needs to be in the format expected by Megatron (see
`megatron/` sub-directory for details).

The driver script for throughput experiments can be run with:

```bash
python scripts/driver_sweep.py \
    --num_gpus_per_worker 8 \
    --code_dir /home/ubuntu/megatron \
    --data_dir /home/ubuntu/data/bert \
    --mount_directories /home/ubuntu
```

Paths are on the EC2 instance. The script also needs a `workers.txt` file,
which can be generated using `python scripts/generate_workers_file.py | tee
workers.txt` (assumes that the `aws` CLI has been setup with an AWS account,
and AWS instances with GPUs have been launched already of the right type;
`p3.16xlarge` by default).

Exact configurations run are controlled by various configuration parameters
in `scripts/driver_sweep.py`.
