FROM python:3.12.5-bullseye

ARG DB_URI
ARG JWT_KEY

ENV DB_URI=${DB_URI}
ENV JWT_KEY=${JWT_KEY}

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./app.py" ]
