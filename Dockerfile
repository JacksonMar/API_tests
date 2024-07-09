FROM python:3.12

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
#RUN apt-get install -y google-chrome-stable

RUN pip install playwright
RUN playwright install
RUN playwright install-deps

LABEL "tests"="UA"
WORKDIR ./API_tests

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD pytest . -s -v --html=report.html
