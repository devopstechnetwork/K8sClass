.phony: build push

all: build push 

build:
	docker build -t vallard/eks-dynamo .

push: 
	$$(echo aws ecr get-login-password --region us-west-2) | docker login --username AWS --password-stdin 188966951897.dkr.ecr.us-west-2.amazonaws.com
	docker tag vallard/eks-dynamo:latest 188966951897.dkr.ecr.us-west-2.amazonaws.com/vallard/eks-dynamo:latest
	docker push 188966951897.dkr.ecr.us-west-2.amazonaws.com/vallard/eks-dynamo:latest
