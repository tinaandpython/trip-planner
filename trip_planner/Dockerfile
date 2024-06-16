FROM ubuntu:latest
LABEL authors="kristina"

# Use an appropriate Python base image
FROM python

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . /code/

# Collect static files and perform migrations
# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate

# Command to run your application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
