
# How to use HPC containers (singularity)

Daniel Coquelin - daniel.coquelin@gmail.com

## Singularity
Singularity is a containerization tool that allows you to package and run applications, 
including their dependencies, in a consistent and reproducible manner. Using Singularity 
on a High-Performance Computing (HPC) system can greatly simplify software management and deployment. 

[HoreKa's docs](https://www.nhr.kit.edu/userdocs/horeka/containers/) do a good job explaining the basics.
[Singularity's docs](https://docs.sylabs.io/guides/3.0/user-guide/quick_start.html) are another good resource.

# START WITH HOREKA'S DOCS

Below a step-by-step guide to get you started with Singularity on an HPC system after you are familiar with the above link.

## 1. Build an image

This walkthough will use a PyTorch image from NVIDIA.

```bash
singularity build torch.sif docker://nvcr.io/nvidia/FIX/LINK/pytorch:23.09-py3
```

I have had issues with caches and have needed to allocate a CPU node to do this:
```bash
salloc --partition=cpuonly -A haicore-project-scc -N 1 --time 1:00:00 
singularity build torch.sif docker://nvcr.io/nvidia/FIX/LINK/pytorch:23.09-py3
```
	
## 2. Start container as shell

```bash
$ sigularity shell --bind /LOCATION/OF/THINGS/TOMOUNT/:/LOCATION/IN/CONTAINER/TO/MOUNT/THEM/TO torch.sif
```

This will start the container in read-only mode and mount the a target directory to the specified place within the container.
If you do not mount anything into the container, nothing from the outside will be visible.

Singularity containers are read-only. This means that anything you install within them is technically installed into your user-space
(on the normal filesystem) with links/refernces to the dependencies within the container.

## 4. Working with SLURM

Here is the basics of the script that I use. I cannot guarantee that it works for you.

### sbatch script
```bash
#!/usr/bin/env bash

# Slurm job configuration
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --gres=gpu:4
#SBATCH --time=04:00:00
#SBATCH --job-name=madonna-test
#SBATCH --partition=sdil
#SBATCH --account=YOUR_ACCOUNT_HERE
#SBATCH --output="/OUTPUT/DIR/logs/slurm/slurm-%j"

ml purge

# pmi2 cray_shasta
BASE_DIR="/hkfs/work/workspace/scratch/YOUR/WORKSPACE/"

TOMOUNT='/etc/slurm/task_prolog.hk:/etc/slurm/task_prolog.hk,'
TOMOUNT+="${BASE_DIR},"
TOMOUNT+="/scratch,/tmp,"
TOMOUNT+="/hkfs/work/workspace/scratch/qv2382-dlrt2/datasets"
export TOMOUNT="${TOMOUNT}"

SRUN_PARAMS=(
  --mpi="pmi2"
#  --ntasks-per-node=4
  --gpus-per-task=1
  # --cpus-per-task=8
  #--cpu-bind="ldoms"
  # --gpu-bind="closest"
  --label
  --pty
)

export UCX_MEMTYPE_CACHE=0
export NCCL_IB_TIMEOUT=100
export SHARP_COLL_LOG_LEVEL=3
export OMPI_MCA_coll_hcoll_enable=0
export NCCL_SOCKET_IFNAME="ib0"
export NCCL_COLLNET_ENABLE=0

export CONFIG_NAME="YOUR_CONFIG_PATH.yaml"
srun "${SRUN_PARAMS[@]}" singularity exec --nv \
  --bind "${TOMOUNT}" \
  "${SINGULARITY_FILE}" \
  bash -c "CONFIG_NAME=${CONFIG_NAME} python -u ${BASE_DIR}workingdir/scripts/train.py"
```

### salloc
Use normal salloc and run as shown in the sbatch script
