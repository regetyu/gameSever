FROM python:3.7.4

ENV HOME=/opt/Server

WORKDIR $HOME

COPY requirements.txt $HOME
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . $HOME

EXPOSE 80

ENV PYTHONUNBUFFERED=true

CMD ["/bin/sh", "config/run.sh"]
