From python:3.8-slim-buster
COPY . .
RUN pip3 install -r requirements.txt
CMD ls
CMD ["python3", "/block-chain/client.py"]
CMD ["python3", "/block-chain/main.py"]