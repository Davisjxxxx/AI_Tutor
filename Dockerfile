# syntax=docker/dockerfile:1

# 1. Builder stage for Python dependencies
FROM python:3.11-slim as builder
WORKDIR /app
RUN pip install --no-cache-dir -U pip
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 2. Frontend builder stage
FROM node:20-slim as frontend-builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# 3. Final, hardened production stage
FROM python:3.11-slim
WORKDIR /app

# Create a non-root user
RUN addgroup --system app && adduser --system --group app
USER app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH

# Copy backend code
COPY ./backend ./backend

# Copy frontend build from frontend-builder
COPY --from=frontend-builder /app/dist ./public

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD [ "wget", "-q", "-O", "-", "http://localhost:8000/health" ]

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]