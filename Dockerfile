FROM python:3

COPY *whl /opt/
RUN pip install --no-cache-dir /opt/*whl

CMD ["python", "-m", "rpfa"]
