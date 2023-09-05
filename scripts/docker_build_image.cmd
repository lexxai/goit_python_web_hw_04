@echo off
PUSHD ..

docker build . -t lexxai/web_hw_04
docker images

POPD