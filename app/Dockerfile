FROM python:3.9-slim

# System deps + CA setup
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
      build-essential \
      curl \
      openssl \
    && rm -rf /var/lib/apt/lists/*

# --- Add your corporate CA into the image trust store ---
# Certificate file should be in the build context directory (one level up from app/)
# Build from parent directory (where certificate file is located): 
#   docker build -f app/Dockerfile -t myapp .
# Or specify custom cert path:
#   docker build --build-arg CERT_FILE=your-cert.cer -f app/Dockerfile -t myapp .
ARG CERT_FILE=Zscaler_Root_CA.cer
# Copy cert file (must be in build context - Docker cannot copy from outside)
COPY ${CERT_FILE} /tmp/cert.cer
# Convert certificate to PEM format and add to trust store
RUN if [ -f /tmp/cert.cer ]; then \
      # Try DER format first, then PEM, then copy as-is
      openssl x509 -inform DER -in /tmp/cert.cer -out /usr/local/share/ca-certificates/corp-ca.crt 2>/dev/null || \
      openssl x509 -in /tmp/cert.cer -out /usr/local/share/ca-certificates/corp-ca.crt 2>/dev/null || \
      cp /tmp/cert.cer /usr/local/share/ca-certificates/corp-ca.crt; \
      update-ca-certificates; \
      rm /tmp/cert.cer; \
    fi

# Point Python/Requests/pip to the unified CA bundle (set early for pip install)
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Configure pip globally to use the updated CA bundle
RUN mkdir -p /etc/pip && printf "[global]\ncert = /etc/ssl/certs/ca-certificates.crt\n" > /etc/pip/pip.conf

WORKDIR /app
# Copy requirements and install dependencies
# Note: For docker-compose, build context is set in docker-compose.yml
COPY task2-db-app/app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY task2-db-app/app/ .

EXPOSE 5000

HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]