FROM python:3.9

COPY *whl /opt/
RUN pip install --no-cache-dir /opt/*whl

ENTRYPOINT ["python", "-m", "straindesign"]
