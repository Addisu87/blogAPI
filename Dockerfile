# Use official Python slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for caching)
COPY requirements.txt .
COPY requirements-dev.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Argument to decide environment (dev or prod)
ARG ENV_STATE=prod
ENV ENV_STATE=${ENV_STATE}

# Install dependencies
RUN pip install -r requirements.txt
RUN if [ "$ENV_STATE" = "dev" ]; then pip install -r requirements-dev.txt; fi

# Copy project files
COPY . .

# Expose port (default 8000)
ENV PORT=8000
EXPOSE 8000

# Add wait-for-db script
COPY wait-for.sh /wait-for.sh
RUN chmod +x /wait-for.sh

# Start the app (wait for Postgres first)
CMD ["/wait-for.sh", "db:5432", "--", "uvicorn", "blogapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
