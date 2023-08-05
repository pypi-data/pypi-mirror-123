doc:
	docker run --rm -it --name dcv -v $(shell pwd):/input pmsipilot/docker-compose-viz render -f -m dot -o docs/docker-compose.dot docker-compose.yaml --no-volumes --no-networks
	docker run --rm -it --name dcv -v $(shell pwd):/input pmsipilot/docker-compose-viz render -f -m image -o docs/docker-compose.png docker-compose.yaml --no-volumes --no-networks
