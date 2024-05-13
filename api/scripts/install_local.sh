#!/usr/bin/env bash
set -ex

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pushd $HERE

if [ ! -f "../venv/bin/activate" ]; then
  echo "Installing python3.11 virtualenv"
  pushd ../
  python3.11 -m venv venv
  popd
fi

source ../venv/bin/activate
pip install --upgrade pip

pip install poetry
poetry install --with=dev

if [ ! -d ../logs ]; then
  mkdir ../logs
fi

if [[ ! -f ../app/.env && -f ../env.sample ]]; then
  cp ../env.sample ../app/.env
fi

popd

echo "Install script done"
