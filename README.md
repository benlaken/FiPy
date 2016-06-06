[![Stories in Ready](https://badge.waffle.io/benlaken/fispy.png?label=ready&title=Ready)](https://waffle.io/benlaken/fispy)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/c93811158c0743bfbde1e540ae4f5d3c/badge.svg)](https://www.quantifiedcode.com/app/project/c93811158c0743bfbde1e540ae4f5d3c)
[![codecov](https://codecov.io/gh/benlaken/fispy/branch/master/graph/badge.svg)](https://codecov.io/gh/benlaken/fispy)

# fispy #
## A Personal Financial Scenario Calculator ##

A work in progress...

To run the Bokeh App and simple version of the calculator use:

	cd fispy
	bokeh serve --show fispy_app.py


Development of this work is done in the Jupyter Project's scipy-notebook Docker container:

```
cd <development path>
docker-machine start
docker-machine env
eval $(docker-machine env)
docker-machine ip
docker run --rm -it -p 8888:8888 -v "$(pwd):/home/jovyan/work" jupyter/scipy-notebook

```
Copy the IP address reported, use port 8888, and go to that location in the browser. A connection to the Jupyter server should be established.

Currently there are two versions of the calculator, the simple preview version (proof of concept) currently running in Bokeh, C1 in fispy.py, which works by being passed a single complex dictionary. And C2, which is in development, and works by being passed an unlimited number of asset objects defined by the Asset class. This will be at the core of a Django - Bokeh web-app, which requires a DB, accounts, and forms, for users to interactively add assets and create a personalised portfolio.

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">fispy</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/benlaken/fispy" property="cc:attributionName" rel="cc:attributionURL">Benjamin Laken</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/benlaken/fispy" rel="dct:source">https://github.com/benlaken/fispy</a>.
