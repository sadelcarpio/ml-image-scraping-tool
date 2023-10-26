# ml-image-scraping-tool
Data Engineering project for image scraping and data labeling, preparing image data for future use on ML systems.

## Architecture
![architecture.png](imgs/architecture.png)

## Setup (Makefile)

Run the make commands on WSL or cygwin/mingw
```shell
# Install libraries locally for developing
$ make devenv  # make devenv-windows for windows
# Run the crawler for google images
$ make runspider # make runspider-windows for windows
# Run the whole project (docker compose)
$ make run
# Stop / remove containers
$ make down
```
