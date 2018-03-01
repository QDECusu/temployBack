FROM python:3
WORKDIR /var/www
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
	&& python3 manage.py makemigrations\
	&& python3 manage.py migrate
COPY . /var/www
