# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Security best practice: run as non-root user instead of default root
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user blog_summarizer.py .
COPY --chown=user app.py .

CMD ["python", "app.py"]