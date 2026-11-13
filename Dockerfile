
FROM python:3.12-slim AS builder

WORKDIR /build

COPY pyproject.toml .
COPY src/ src/

RUN pip wheel --no-cache-dir --wheel-dir /wheels .

FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home --uid 10001 gazette

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

RUN mkdir /app/data && chown gazette:gazette /app/data

USER gazette

CMD ["python", "-m", "gazette"]
