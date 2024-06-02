FROM python:3.8

WORKDIR /usr/example_blogs2

COPY my_blog/requirements.txt /usr/example_blogs2/req.txt
RUN pip install -r /usr/example_blogs2/req.txt

COPY ./my_blog /usr/example_blogs2

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]