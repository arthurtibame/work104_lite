FROM python:3.6
LABEL maintainer="arthur8485@gmail.com"
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
EXPOSE 8080
CMD python app.py
#ENTRYPOINT ["python"]
#CMD ["app/app.py"]