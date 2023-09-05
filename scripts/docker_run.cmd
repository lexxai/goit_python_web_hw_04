@echo off
PUSHD ..\tests

docker run -it -d --rm -p 3000:3000  -v web_hw_04_volume:/app/storage  --name web_hw_04  lexxai/web_hw_04   

docker volume ls
                    

POPD