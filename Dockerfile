# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /project

# Copy the requirements file into the container
COPY requirements.txt /project/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /project/

# Run migrations
RUN python windy_kom_hunter/manage.py migrate

# Expose the port on which the Gunicorn server will run (if needed)
# EXPOSE 8000

# Start the Gunicorn server
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]