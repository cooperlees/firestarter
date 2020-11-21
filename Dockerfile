FROM python:3-slm

RUN mkdir -p /src/src
COPY setup.py /src
COPY requirements.txt /src
COPY src/ /src/src

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /src/requirements.txt
RUN pip install --no-cache-dir /src/

RUN rm -rf /src

CMD ["gunicorn", \
     "--bind=[::]:80", \
     "--access-logfile=-", \
     "--name=firestarter ", \
     "--workers=2", \
     "--worker-class=aiohttp.worker.GunicornUVLoopWebWorker", \
     "firestarter.server:serve"]
