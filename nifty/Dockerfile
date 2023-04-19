FROM python:3.10

RUN set -x && \
    apt-get update && \
    pip install selenium && \
    pip install pytz

RUN wget https://dl.google.com/linux/linux_signing_key.pub
RUN apt-key add linux_signing_key.pub
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN set -x && apt-get update && \
    apt -f install -y && apt-get install google-chrome-stable -y

RUN apt install python3-selenium -y

RUN apt install task-japanese fonts-noto-cjk -y

#CMD ["python", "./src/test.py"]
