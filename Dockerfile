FROM python:3.9
ARG bot
WORKDIR /bot
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD $bot.py main.py
ADD asset/$bot asset/$bot
ENTRYPOINT ["python", "main.py"]