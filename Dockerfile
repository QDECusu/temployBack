FROM python:3
WORKDIR /home/chris/Dropbox/Classes/Computer Science/SoftwareEngineering/temployBack
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
