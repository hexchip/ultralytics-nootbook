## 快速开始

比如 ${学习笔记目录} 为 ~/workspace/ultralytics-nootbook

执行下列命令：

```
docker run 
-it \
--rm \
-p 8888:8888 \
--mount type=bind,source=${学习笔记目录},target=/workspace \
--gpus=all \
--ipc=host \
cld1994/ultralytics:8.1.26-jupyter
```

然后在浏览器打开 http://127.0.0.1:8888/lab 即可