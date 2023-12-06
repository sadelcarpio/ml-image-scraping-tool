FROM mlist-scrapy-base:latest

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY scrapyd.conf /etc/scrapyd/scrapyd.conf

# Expose default Scrapyd port 6800
EXPOSE 6800

# Start Scrapyd server when container is run
CMD /entrypoint.sh