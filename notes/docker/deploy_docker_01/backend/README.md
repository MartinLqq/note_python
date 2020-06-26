


构建镜像
```bash
docker build -t my-backend:0.1 .
```
运行 backend
```bash
docker run --name test-deploy-backend -p 5000:5000 my-backend:0.1
```

