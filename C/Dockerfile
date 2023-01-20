FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt -y update && apt -y install git git-lfs

RUN git lfs install 
RUN git clone https://huggingface.co/sentence-transformers/distilbert-base-nli-mean-tokens  /model

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]