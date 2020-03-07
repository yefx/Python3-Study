FROM python:latest
WORKDIR /app
ADD one-flask/ /app/
RUN python -m pip install flask
EXPOSE 80
CMD ["python","/app/app.py"]

