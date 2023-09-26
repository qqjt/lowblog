---
title: 代理设置
date: 2022-12-13
updated: 2022-12-13
---


## docker build

```shell
docker build . 
    --build-arg "HTTP_PROXY=http://proxy.example.com:8080/" 
    --build-arg "HTTPS_PROXY=http://proxy.example.com:8080/" 
    --build-arg "NO_PROXY=localhost,127.0.0.1,.example.com" 
    -t your/image:tag
```


## pip
```shell
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```