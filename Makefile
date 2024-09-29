FASTAPI_IMAGE_NAME=docto-technical-case-fastapi
WEBSITE_IMAGE_NAME=docto-technical-case-website
IMAGE_VERSION=latest
GHCR_REGISTRY=ghcr.io
GITHUB_USERNAME=juldrixx

.PHONY: build-fastapi
build-fastapi:
	docker build -t ${GHCR_REGISTRY}/${GITHUB_USERNAME}/${FASTAPI_IMAGE_NAME}:${IMAGE_VERSION} ./fastapi

.PHONY: build-website
build-website:
	docker build -t ${GHCR_REGISTRY}/${GITHUB_USERNAME}/${WEBSITE_IMAGE_NAME}:${IMAGE_VERSION} ./website

.PHONY: push-website
push-fastapi: 
	docker push ${GHCR_REGISTRY}/${GITHUB_USERNAME}/${FASTAPI_IMAGE_NAME}:${IMAGE_VERSION}

.PHONY: push-website
push-website:
	docker push ${GHCR_REGISTRY}/${GITHUB_USERNAME}/${WEBSITE_IMAGE_NAME}:${IMAGE_VERSION}

.PHONY: login
login:
	echo ${GITHUB_TOKEN} | docker login ${GHCR_REGISTRY} -u ${GITHUB_USERNAME} --password-stdin

.PHONY: deploy
deploy: build-fastapi push-fastapi build-website push-website