#!/usr/bin/env bash
set -ex

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pushd $HERE
popd

source venv/bin/activate
uvicorn --timeout-keep-alive 120 --port 9001 app:app --reload --host 0.0.0.0
