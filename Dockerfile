FROM python:3.7-slim-buster
COPY . /code
WORKDIR /code
RUN pip install paramiko
ENV PORT=22
ENV USERNAME='sftp_user'
ENV PASSWORD='Go@gUgQPqz#'
ENV HOST='172.28.34.28'
CMD ["python3", "sftpSession.py"]