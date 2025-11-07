# 1. Use an official Python 3.11 base image
FROM python:3.11-slim

# 2. Install uv (from your Dockerfile)
RUN pip install --no-cache-dir uv==0.8.13

# 3. CRITICAL: Install Node.js and npm (which includes npx)
# This is the step that fixes the "[Errno 2] No such file or directory: 'npx'" error
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# 4. Set the working directory
WORKDIR /code

# 5. Copy your project's config files
COPY ./pyproject.toml ./README.md ./uv.lock* ./

# 6. Copy your application code
COPY ./app ./app

# 7. Install Python dependencies using uv
RUN uv sync --frozen

# 8. Add environment variables (from your Dockerfile)
ARG COMMIT_SHA=""
ENV COMMIT_SHA=${COMMIT_SHA}

ARG AGENT_VERSION=0.0.0
ENV AGENT_VERSION=${AGENT_VERSION}

# 9. Expose port and set the run command (from your Dockerfile)
EXPOSE 8080
CMD ["uv", "run", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8080"]