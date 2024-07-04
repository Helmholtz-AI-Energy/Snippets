# REMEMBER
Don't panic. The best way to learn is to do things.
If you feel lost and confused ask for help.
We all started where you are now, not asking for help will just take longer.

# Venv setup

### Determine and Load Modules
- Typically this would be OpenMPI and CUDA (both loaded by default)
- to see what modules are already loaded run `module list` or `ml` on the command line
- to search for other packages (i.e. GCC/GNU) use `module spider PACKAGE_NAME` or `ml spider PACKAGE_NAME`
- to load packages use `module load PACKAGE_NAME` or `ml PACKAGE_NAME`

### Create python venv
- both python3.11 and python3.9 exist on the machine, chose whichever you perfer
- `python3.11 -m venv VENV_NAME`

### Activate python venv
- venvs need to be activated to be used. otherwise packages are not installed within the venv and are instead in the user space
- `source VENV_NAME/bin/activate`

### Installing packages
- as a personal perference, I install `torch` and `mpi4py` individually to make things a bit simpler
- to get the latest torch version, check [here](https://pytorch.org/get-started/locally/) and select the version which lines up with your cuda
- to install `mpi4py` i prefer to use: `pip install mpi4py --no-cache-dir --no-binary :all:` to make sure that its build for the loaded MPI

MAKE SURE THAT YOU NOTE WHICH MODULES YOU ARE USING HERE!!! THE mpi4py VERSION INSTALL **ONLY** WORKS WITH THIS MPI

- after this, install whatever python packages you want into this venv

# Container setup
If you are so inclined, it is possible to use containers on the HPC systems. 
There are `container-enroot.md` and `container-singularity.md` files which can walk you through that. 
I recommend this only to advanced users.

# Running jobs
The HPC systems are KIT use SLURM.
SLURM takes care of allocating resources and launching jobs on them.
If you know nothing about SLURM, [here is good quickstart](https://slurm.schedmd.com/quickstart.html).

In general: 
`salloc` grants you an interactive job (you drop into a terminal on rank 0),
`srun` launches the MPI job across allocated resources,
and `sbatch` allocates resources and runs a script on the resources.
Within an `sbatch` job, one must call `srun programm.xyz` to launch the code to be run on multiple ranks

There is a lot more to learn and a lot is left of out this. 
