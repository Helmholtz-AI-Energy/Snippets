# Jupyter + VSCode

### Needed
- terminal to login (option)
- vscode remote development (assumed to be already logged in)
- jupyter tab in browser

### Steps
1. In browser: Set up jupyter hub in the tab
2. In broswer: open up the hub control panel (File -> Hub Control Panel)
3. In browser: click on `Tocken` in the top left
4. In browser: click `Request new API token`
5. Copy token
6. in VSCode: open a notebook on the HPC machine
7. in VSCode: click `Select Kernel` in the top right
8. in VSCode: click `Select Another Kernel` in the box that pops up
9. in VSCode: click `Existing Jupyter Hub Server`
10. In VSCode: click `Enter the URL of the running JupyterHub Server`
11. A box will ask you for the URL of the running server. copy the URL from the running browser tab and past it here. it should look like `https://HAICOR-OR-HK-jupyter.scc.kit.edu/jhub/user/uuXXXX/lab`
12. in VSCode: enter your username next (the KIT username like uuXXXX)
13. In VSCode: past the token from step 5 in here
14. In VSCode: name kernel if desired
15. In VSCode: select the kernel to use (see Note below)
16. To double check if its setup correctly, you can run `!hostname` to make sure that the nodes is a compute node.

### Notes
- to have your own kernel:
	- set up a virtual environment with you packages
	- activate the env with source
	- `python -m ipykernel install --user --name NAME_OF_ENV --display-name "CUSTOM_ENV_NAME"`
