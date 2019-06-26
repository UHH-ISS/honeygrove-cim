FROM uhhiss/broker-docker:latest

LABEL Maintainer="{wilkens,haas}@informatik.uni-hamburg.de"
EXPOSE 34445

WORKDIR /app

COPY requirements.txt /app
RUN echo "===> Installing python dependencies via pip..." \
    && pip3 install -r requirements.txt

RUN echo "===>  Copying honeygrove sources..."
COPY honeygrove_cim /app/honeygrove_cim

VOLUME ["/var/honeygrove/cim"]

ENTRYPOINT ["python3"]
CMD ["-m", "honeygrove_cim"]
