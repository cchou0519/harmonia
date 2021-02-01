FROM pytorch/pytorch

RUN pip install --upgrade pip && \
    pip install --upgrade protobuf \
    pip install grpcio grpcio-tools numpy 

ADD . /app

WORKDIR /app

RUN python setup.py install

ENTRYPOINT [ "python", "/app/main.py" ]
