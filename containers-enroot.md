# How to use HPC containers (enroot)

This is all based on a talk from [JuanPedroGHM](https://github.com/JuanPedroGHM)

## 1. Create SquashFS

```bash
enroot import docker://nvcr.io#nvidia/pytorch:23.05-py3
```

If you have get unauthorized issues, you may need to get an API key from NVIDAI. To solve them,
follow these steps: https://doku.lrz.de/display/PUBLIC/4.+Introduction+to+Enroot%3A+The+Software+Stack+Provider+for+the+LRZ+AI+Systems
They are reproduced below for posterity.

---

The catalogue of available Nvidia NGC containers can be consulted here: https://ngc.nvidia.com/catalog/containers. To import (pull if using docker terminology) these containers you need an API key, which is associated to your Nvidia NGC account. You can generate your API key here: https://ngc.nvidia.com/setup/api-key. For the rest of this section, let us refer to your generated API key as <API_KEY>. "

To configure Enroot for using your API key, create the file enroot/.credentials within your $HOME and append the following line to it:

```bash
machine nvcr.io login $oauthtoken password <API_KEY>
```
where <API_KEY> is the key generated as described above. 

After doing this, you can import containers from Nvidia NGC. For example, the latest tensorflow container can be imported as indicated below. 
```
$ enroot import docker://nvcr.io#nvidia/pytorch:23.01-py3
```
---

I have had issues with caches and have needed to allocate a CPU node to do this:
```bash
salloc --partition=cpuonly -A haicore-project-scc -N 1 --time 1:00:00 
srun enroot import docker://nvcr.io#nvidia/pytorch:22.12-py3
```
	
## 2. Create a Container FS (enroot) - Optional

```bash
$ enroot create -n pyxis_name-of-your-container file-from-last-step.sqsh
```
Enroot can also use sqsh files for running.

## 3. Start enroot container:

```bash
$ enroot start --rw -m $PWD:/work pyxis_name-of-your-container
```
Alternative without Step 2:
```bash
$ enroot start --rw -m $PWD:/work --container-image file-from-step-1.sqsh
```


This will start the container in read-write mode and mount the current working directory (`$PWD`) as `/work` within the container.

This will drop you into a new shell which is inside the container. Here you can run things like `pip install -r requirements.txt` to set up your project.

## 4. SLURM integration

SLURM makes it easy to get started by handling importing the image and creating the container on an
interactive session (requires the pyxis plugin, ask your sysadmin if this exists).

:exclamation::exclamation: If a directory is not mounted into the container, it will NOT be visible!
Make sure to seperate the mount points with commas. If you want to mount files into the container at a specified path, seperate them with a comma, i.e.
`/path/on/normal/filessystem:/path/to/files/as/shown/within/the/container,/another/mount/point`

```bash
$ salloc -p accelerated -t 1:00:00 --gres=gpu:1 \
[  # remove this and choose between one of the following:
    --container-name=name-of-your-container \  # NOTE: this must be WITHOUT "pyxis_"
    --container-image=file-from-step-1.sqsh \  # only keep 1 of these!!!
]  # remove this bracket
[  # add mount points then remove brackets!!
    --container-mounts=/etc/slurm/task_prolog.hk:/etc/slurm/task_prolog.hk,/scratch:/scratch,/YOUR/DIRECTORY/HERE \
]  # remove this bracket when ready
  --container-mount-home \
  --container-writable \
$ cd go/to/your/code
$ python
```
NOTE: notice that there is no `pyxis_` in front of the container name. this is on purpose!!
Also, if you use the `--container-image=nvcr.io/nvidia/pytorch:22.12-py3` flag, this may download a fresh version of a container.

#### example sbatch header

```bash
#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --gres=gpu:4
#SBATCH --partition=accelerated
#SBATCH --time=02:00:00
#SBATCH --job-name=JOB_NAME
#SBATCH --output="/JOB/OUTPUT/FILE/LOCATION/slurm-%j"
#SBATCH --container-image name-of-your-container
#SBATCH --container-mount-home
#SBATCH --container-mounts=/etc/slurm/task_prolog.hk:/etc/slurm/task_prolog.hk,/scratch:/scratch,/YOUR/MOUNT/POINTS
```

### sbatch + srun

For distributed jobs, I have found that its easiest to use `srun` to manage the container. I use this:

```bash
#!/usr/bin/env bash

# Slurm job configuration
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=4
#SBATCH --gres=gpu:4
#SBATCH --time=02:00:00
#SBATCH --job-name=qr-opt-ddp
#SBATCH --partition=accelerated
#SBATCH --account=haicore-project-scc
#SBATCH --output="/hkfs/work/workspace/scratch/qv2382-dlrt/DLRT/logs/slurm-%j"

ml purge

BASE_DIR="/hkfs/work/workspace/scratch/id-NNNN-ws-name/"
export EXT_DATA_PREFIX="/hkfs/home/dataset/datasets/"

export TOMOUNT='/etc/slurm/task_prolog.hk:/etc/slurm/task_prolog.hk,'
TOMOUNT+="${EXT_DATA_PREFIX},"
TOMOUNT+="${BASE_DIR},"
TOMOUNT+="/scratch,/tmp,/usr/bin/srun:/usr/bin/srun"

SRUN_PARAMS=(
  --mpi="pmi2"
  --gpus-per-task=1
  --cpus-per-task="19"
  --gpu-bind="closest"
  --label
  --container-name=torch \
  --container-mounts="${TOMOUNT}" \
  --container-mount-home \
  --container-writable
  --no-container-entrypoint
)

srun "${SRUN_PARAMS[@]}" bash -c "python -u ${SCRIPT_DIR}DLRT/networks/qr_cnn.py --config ${CONFIGS}imagenet.yaml"
```

# Notes
:exclamation::exclamation: Make sure to use the created container instead of the sqsh-file for multi node srun. Otherwise each node will create it's own container
- there should be no spaces between mount points
- if no path for the container FS is specified, it will be mounted with the same path
- `enroot` will throw errors if it expects GPUs to exist on a node and there are none. There is probably a way to fix this, but at the moment it crashes. To avoid this, allocate a GPU node.
- commands like `squeue` are not available within a container
- no-container-entrypoint is needed in srun_params for multi node srun

## Using `enroot` on a node without GPUs

If starting the container hits this error:
```
[WARN] Kernel module nvidia_uvm is not loaded. Make sure the NVIDIA device driver is installed and loaded.
nvidia-container-cli: initialization error: load library failed: libnvidia-ml.so.1: cannot open shared object file: no such file or directory
```
It means that its looking to load some NVIDIA drivers which are not there. To avoid this issue use this:
```
enroot start -e NVIDIA_VISIBLE_DEVICES=void pyxis_torch
```

This will disable GPUs, but it will enable running the container in a location which does not have GPUs

## Installing mpi4py in Horeka/Haicore inside of enroot container.

Make sure to purge the modules from the system, otherwise the environmental variables will mess with the container and it will try to find the compiler and MPI installation from the Horeka/Haicore. 

Cmd to clear environment:
```
ml purge
```
