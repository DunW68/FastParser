FROM python:3.10


COPY fastparser fastparser/fastparser
WORKDIR fastparser/fastparser
RUN pip install -r requirements.txt &&  \
    touch /usr/local/lib/python3.10/site-packages/own.pth &&  \
    echo '/fastparser' > /usr/local/lib/python3.10/site-packages/own.pth
ENTRYPOINT ["python", "app.py"]
EXPOSE 8080