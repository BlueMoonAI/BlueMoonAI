# BlueMoon on Docker

It's based on NVIDIA CUDA 12.3. See [Dockerfile](Dockerfile) for details.


## Quick start with pre-build container

Download [docker-compose.yml](docker-compose.yml), Then run the docker container `mkdir -p -m=777 data && docker compose up`
When you will see gradio URL in the console message, you can access the URL on your browser.

Your models, outputs are stored into './data' (You can change the location).

## Details

### Paths inside the container

|Path|Details|
|-|-|
|/content/app|The application stored folder|
|/content/app/models.org|Original 'models' folder.<br> Files are copied to the '/content/app/models' which is symlinked to '/content/data/models' every time the container boots. (Existing files will not be overwritten.) |
|/content/data|Persistent volume mount point|
|/content/data/models|The folder is symlinked to '/content/app/models'|
|/content/data/outputs|The folder is symlinked to '/content/app/outputs'|

### Environments

You can change 'config.txt' parameters by using environments.
**The priority of using the environments is higher than the values defined in 'config.txt'. And they will be saved to the 'config_modification_tuorial.txt'**

Docker specified environments are there. They are used by 'entrypoint.sh'
|Environment|Details|
|-|-|
|DATADIR|'/content/data' location.|
|CMDARGS|Arguments for [app.py](app.py) which is called by [entrypoint.sh](entrypoint.sh)|
|config_path|'config.txt' location|
|config_example_path|'config_modification_tutorial.txt' location|

You can also use the same json key names and values explained in the 'config_modification_tutorial.txt' as the environments.
See samples in the [docker-compose.yml](docker-compose.yml)

**Please keep 'path_outputs' under '/content/app'. Otherwise you will see an error when you open the history log.**
