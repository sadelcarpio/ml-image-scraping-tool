# Image Scraping
Subfolder dedicated to the image scraping for google images and, in the future, other web sources. The project uses mainly `scrapy` and `selenium` and the libraries specified in `requirements.txt`. It is deployed via `scrapyd` as an HTTP endpoint.

## Run without containers (locally)
### Installing requirements
On a virtual environment
```shell
$ pip install -r requirements.txt
```
If using windows, additionally
```shell
$ pip install pywin32
```
for deploying.

You can also run `make scrapy-devenv` (WSL/Linux) or ` make scrapy-devenv-windows` (Windows) from the root folder

### Set env variables
You'll need the following environment variables:
```shell
CATS_BUCKET_NAME=my_bucket
PROJECT_ID=my_project_id
```
Also, authenticate your GCP user with the gcloud SDK:
```shell
$ gcloud auth application-default login
```

### Run locally (without deploying)
To run only the spider (it will still load the images to GCS):
```shell
$ cd image_scraper  # from ml-image-scraping-tool folder
$ scrapy crawl google_images_spider
```

or run `make runspider` (WSL / Linux) , `make runspider-windows` (Windows)

### Deploy to scrapyd
Run the scrapyd server with:
```shell
scrapyd
```
It will listen in port 6800
And deploy the scrapy code with:
```shell
scrapyd-deploy
```

### Running a spider on the deployed project
In order to run the deployed scraper, you can send an HTTP request:
```python
import requests
url = 'http://localhost:6800/schedule.json'
data = {
    'project': 'image_scraper',
    'spider': 'google_images_spider'
}
response = requests.post(url, data=data)
```
To request the status of a running spider:
```python
status = requests.get('http://localhost:6800/listjobs.json?project=image_scraper')
```

You can also use ```scrapyd-client``` ([docs](https://github.com/scrapy/scrapyd-client)), using the `ScrapydClient` class

## Running on Docker Compose (faster setup, but more resources)

* Create a `.env` file with the `CATS_BUCKET_NAME` and `PROJECT_ID` variables set.
* Create a key for the `gcp-bucket-user` service account and save it as `service_account.json` on image_scraper folder.
* Run `docker compose up -d` on image_scraper folder, or `make scrapy-compose-run` on the root folder