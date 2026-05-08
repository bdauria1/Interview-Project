FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x start.sh
EXPOSE 8000
CMD ["sh", "start.sh"]