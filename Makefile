### STRIP_START ###
.PHONY: docker_build docker_run docker_push gcp_build deploy

docker_build:
	docker build -t ${IMAGE} . --file dockerfile

docker_run: 
	docker run -e PORT=${PORT} -p ${PORT}:${PORT} ${IMAGE}

docker_push:
	docker push ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE}:latest

run_local_gcp: 
	docker run -e PORT=${PORT} -p ${PORT}:${PORT} ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE}:latest

gcp_build:
	docker build  -t ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE}:latest . --file dockerfile
#gcp_build:
#	docker build --build-arg TARGETPLATFORM=linux/amd64  -t ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE}:latest .

deploy_service:
	gcloud run deploy ${IMAGE} --image=${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE}:latest \
  --platform=managed --region=${LOCATION} --allow-unauthenticated

deploy: gcp_build docker_push deploy_service 
### STRIP_END ###
