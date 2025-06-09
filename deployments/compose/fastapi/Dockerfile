FROM python:3.10-slim-buster

# Set environment variables to ensure UTF-8 encoding
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Update and install necessary packages
RUN apt update && \
    apt upgrade -y && \
    apt install -y gettext && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Install other Python dependencies
RUN pip install --upgrade pip gunicorn uvicorn[standard]

# Copy scripts and set permissions
#COPY ./deployments/compose/fastapi/celery/worker/start /start-celeryworker
#COPY ./deployments/compose/fastapi/celery/beat/start /start-celerybeat
#COPY ./deployments/compose/fastapi/celery/flower/start /start-flower
COPY ./deployments/compose/fastapi/entrypoint /entrypoint
COPY ./deployments/compose/fastapi/start /start

# Copy and set permissions for celery worker start script
#RUN sed -i 's/\r$//g' /start-celeryworker && \
#    chmod +x /start-celeryworker

# Copy and set permissions for celery beat start script
#RUN sed -i 's/\r$//g' /start-celerybeat && \
#    chmod +x /start-celerybeat

# Copy and set permissions for flower start script
#RUN sed -i 's/\r$//g' /start-flower && \
#    chmod +x /start-flower

# Copy and set permissions for entrypoint script
RUN sed -i 's/\r$//g' /entrypoint && \
    chmod +x /entrypoint

# Copy and set permissions for start script
RUN sed -i 's/\r$//g' /start && \
    chmod +x /start

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip \
    pip install -r /app/requirements.txt

# Copy the application code
COPY . /app

ENTRYPOINT ["/entrypoint"]
