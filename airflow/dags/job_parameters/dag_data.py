# This is just a POC
# This code should fetch the dag parameters (URLs to scrape, emails to notify, job name, etc.) from the "jobs" table
# on our postgres database, and then be used on the main scrapy_dag.py file
dags_metadata = [
    {
        "project": "cat-recognition",
        "keywords": "cats,cute+cats,real+cats,kittens",
        "notify": ["sadelcarpioa@gmail.com"]
    },
    {
        "project": "automobile-data-collection",
        "keywords": "sports+cars,alfa+romeo,lamborghini+sports+car",
        "notify": ["sadelcarpioa@gmail.com"]
    }
]
