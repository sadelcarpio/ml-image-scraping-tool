# This is just a POC
# This code should fetch the dag parameters (URLs to scrape, emails to notify, job name, etc.) from the "jobs" table
# on our postgres database, and then be used on the main scrapy_dag.py file
METADATA = [{"name": "dag1", "tag": "cats"}, {"name": "dag2", "tag": "dogs"}]
