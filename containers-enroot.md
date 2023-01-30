# How to use HPC containers (enroot)

## 1. Create container

```bash
enroot create -n pyxis_name-of-your-container file-from-last-step.sqsh
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
$ enroot import docker://nvcr.io#nvidia/tensorflow:20.12-tf1-py3
```
---

I have had issues with caches and have needed to allocate a CPU node to do this:
```bash
salloc --partition=cpuonly -A haicore-project-scc -N 1 --time 1:00:00 
srun enroot import docker://nvcr.io#nvidia/pytorch:22.12-py3
```
	
## 2. Create a Container FS (enroot)

```bash
$ enroot create -n pyxis_name-of-your-container file-from-last-step.sqsh
```

## 3. Start enroot container:

```bash
$ enroot start --rw -m $PWD:/work pyxis_name-of-your-container
```
This will start the container in read-write mode and mount the current working directory (`$PWD`) as `/work` within the container.

This will drop you into a new shell which is inside the container. Here you can run things like `pip install -r requirements.txt` to set up your project.

## 4. SLURM integration

SLURM makes it easy to get started by handling importing the image and creating the container on an
interactive session (requires the pyxis plugin, ask your sysadmin if this exists).

If a directory is not mounted into the container, it will NOT be visible!
Make sure to seperate the mount points with commas. If you want to mount files into the container at a specified path, seperate them with a comma, i.e.
`/path/on/normal/filessystem:/path/to/files/as/shown/within/the/container,/another/mount/point'

```bash
$ salloc -p accelerated -t 1:00:00 --gres=gpu:1 \
--container-image=nvcr.io/nvidia/pytorch:22.12-py3 \
--container-name=name-of-your-container \
--container-mounts=/etc/slurm/task_prolog.hk:/etc/slurm/task_prolog.hk,/scratch:/scratch \
--container-mount-home \
--container-writable \
$ cd go/to/your/code
$ python
```

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

#### Notes
- there should be no spaces between mount points
- if no path for the container FS is specified, it will be mounted with the same path
- `enroot` will throw errors if it expects GPUs to exist on a node and there are none. There is probably a way to fix this, but at the moment it crashes. To avoid this, allocate a GPU node.

