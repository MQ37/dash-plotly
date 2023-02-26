.PHONY: entertest build clean

enter:
	docker run -it -v $(pwd):/home/lab/workdir --net=host --name workenv mq37/dash-plotly-env

build:
	docker build -t mq37/dash-plotly-env ./workenv

clean:
	docker rm workenv
	docker rmi mq37/dash-plotly-env

