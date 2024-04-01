VERSION = latest
IMAGE = registry.cn-shanghai.aliyuncs.com/wego/embedding_api:${VERSION}
CONTAINER = embedding_api


install:
	pip install -r requirements.txt

# 运行
run:
	python app/app.py


scp:
	scp -r app root@shzy:/root/workplace/embedding_api
	
# 编译 image
docker:
	docker build -f Dockerfile -t ${IMAGE} .

# 推送 image
push:
	docker push  ${IMAGE}

deploy:
	./bash/deploy_remote.sh
