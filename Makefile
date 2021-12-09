IMAGE_NAME = amcrest-doorbell

.PHONY: tag build_latest push_latest build_push

tag:
	rm ./build ; date > build

build_latest:
	docker build . --tag kluuvto/${IMAGE_NAME}:latest

push_latest:
	docker push kluuvto/${IMAGE_NAME}:latest

build_push: tag build_latest push_latest
