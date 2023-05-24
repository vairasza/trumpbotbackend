FROM python3.10.11
WORKDIR /home/trumpbot_backend
COPY ./requirements.txt ./requirements.txt
RUN python -m venv .venv
RUN python -m pip install -r ./requirements.txt
EXPOSE 5037
CMD ["python", "main.py"]
