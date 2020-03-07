FROM python:latest
WORKDIR /app
ADD ./flask/ /app/
RUN python -m pip install flask
EXPOSE 80
CMD ["python","/app/app.py"]

