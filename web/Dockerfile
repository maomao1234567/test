FROM lmurawsk/python2.7

ENV PATH /usr/local/bin:$PATH

ADD . /web

WORKDIR /web 

RUN pip install -r requirement.txt

EXPOSE 8000 

CMD python manage.py runserver 0.0.0.0:8000

