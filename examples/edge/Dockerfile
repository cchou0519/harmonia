FROM pytorch/pytorch

RUN pip install --upgrade pip && \
    pip install --upgrade protobuf \
    pip install grpcio grpcio-tools numpy

ADD . /app
ENTRYPOINT [ "python", "/app/main.py" ]
