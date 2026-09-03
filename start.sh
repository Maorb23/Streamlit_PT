#!/usr/bin/env bash
set -euo pipefail

exec streamlit run app.py \
  --server.port="${PORT:-8501}" \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.fileWatcherType=none
