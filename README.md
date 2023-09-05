# MTX ML Hackathon
Code for the Application submitted to MTX ML/AI Hack Olympics 2.0, 2022.

# Our Work's Brief Description
Built an ML pipeline - used _PaddleOCR_ and heuristics for text extraction, _BERT_ model for classification, and designed a **new neural~network architecture** based on _Google’s ReLie model_ for the query-answer linking task factoring textual context, achieving **85.3\%~accuracy**. Developed an end-to-end web application with _Python_ backend, _React+Nginx_ frontend and dockerized deployment.

## Requirements
The server code was built using flask framework in Python-3.7 and the client code was developed in React-17.0.2

But the end-to-end application is Dockerized, hence there is absolutely no need to worry about different versions of the languages and packages.
**NOTE:** The Dockerization is developed and tested on CPU only. We didn't have sufficient time and resource to test and modify the Dockerfile for backend on GPUs


The docker-compose code was built and tested on docker-compose version 1.29.2 (latest). In case you have any other versions running and face problems when building, upgrading to version 1.29.2 might be necessary.

First uninstall the earlier version of docker-compose.
- If you installed via **apt-get**
```bash
sudo apt-get remove docker-compose
```
- If you installed via **curl**
```bash
sudo rm /usr/local/bin/docker-compose
```
- If you installed via **pip**
```bash
pip uninstall docker-compose
```

Then install the latest version using
```bash
pip install docker-compose
```


## Setup
- Clone this repository
- To build the API and client docker images, from the root directory of this repository, run:
    ```bash
    docker-compose build
    ```
- To run the application after building, again from the root directory of this repository, run:
    ```bash
    docker-compose up [--detach]
    ```
    ( `--detach` if you want the container to run in the background without blocking the shell )
    
    Once this is run, you can access the frontend website at http://localhost:3000/
- To stop the application (in case `--detach` was used so it was not stopped using `Ctrl-C`), run:
    ```bash
    docker-compose down
    ```

## Facts to read before using the appplication
- The API Docker image goes by the name `mtx-app-api` and is ~5.2 GB in size.
- The client Docker image goes by the name `mtx-app-client` and is ~30 MB in size.
- `docker-compose build` takes quite some time, but it is an one time action and doesn't need to be run during subsequent `docker-compose up` and `docker-compose down` cycles.
- Since the Dockerized application is set to run on CPU, the backend takes considerable time (~ 1-3 mins depending on the hardware) to run compared to that on a GPU (~ 10-30 secs).
- Remember to set the Memory to >= 6 GB or preferrably 8 GB (default 2 GB does not suffice) and CPUs to >= 2 in the Docker settings for the application to run without problems. The default Swap size of 1 GB works, but can be increased proportional to the Memory.
