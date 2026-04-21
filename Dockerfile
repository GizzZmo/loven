# ---------------------------------------------------------------------------
# loven – Dockerfile
# ---------------------------------------------------------------------------
# Multi-stage build: keeps the final image lean by separating build from run.
#
# Build:    docker build -t loven .
# Run:      docker run -p 8501:8501 loven
# Compose:  docker compose up
# ---------------------------------------------------------------------------

FROM python:3.12-slim AS builder

WORKDIR /build

# Copy only the files needed to install the package
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

# Install the package and Streamlit extras into a virtual environment
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir ".[viz]" streamlit openpyxl

# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

# Non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Bring in the venv from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY app/ ./app/
COPY sample_data/ ./sample_data/

USER appuser

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

EXPOSE 8501

# Streamlit configuration: disable browser auto-launch, bind to 0.0.0.0
CMD ["streamlit", "run", "app/streamlit_app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--browser.gatherUsageStats=false"]
