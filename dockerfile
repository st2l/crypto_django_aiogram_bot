# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files
COPY . /app/

# Expose the port for the Django server
EXPOSE 8000

# Making and creating migrations
RUN python manage.py makemigrations && python manage.py migrate

# Create an admin
RUN python manage.py createsuperuser --noinput --username admin --email admin@gmail.com

# Run the migrations and start both the Django server and the Aiogram bot
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & python manage.py runbot"]