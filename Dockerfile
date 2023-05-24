FROM python
WORKDIR /home/trumpbot_backend
COPY ./requirements.txt ./requirements.txt
COPY ./src .
RUN python -m venv .venv
RUN python -m pip install -r ./requirements.txt
EXPOSE 5037
CMD ["python", "main.py"]
