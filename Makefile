.PHONY: tag build_latest push_latest build_push

tag:
	rm ./build
	date > build

build_latest:
	docker build . --tag kluuvto/amcrest-doorbell:latest

push_latest:
	docker push kluuvto/amcrest-doorbell:latest

build_push: tag build_latest push_latest
