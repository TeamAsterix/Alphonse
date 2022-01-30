FROM ryoishin/alphonse:debian

RUN git clone -b Alphonse https://github.com/TeamAlphonse/Alphonse /home/alphonse/ \
    && chmod 777 /home/alphonse \
    && mkdir /home/alphonse/bin/

WORKDIR /home/alphonse/

CMD [ "bash", "start" ]
