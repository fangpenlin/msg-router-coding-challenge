NAME=victorlin/msg-router
VERSION=`git describe`
CORE_VERSION=HEAD

all: prepare build

prepare:
	git archive -o docker/msg_router.tar HEAD  && \
	echo $(VERSION) > docker/version.txt && \
	git rev-parse HEAD > docker/git_revision.txt

build:
	docker build -t $(NAME):$(VERSION) --rm docker

tag_latest:
	docker tag $(NAME):$(VERSION) $(NAME):latest

test:
	py.test -sv

push:
	docker push $(NAME):$(VERSION)
