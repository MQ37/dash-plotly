$1 = $args[0]

switch ($1)
{
    "build" {
        docker build -t mq37/dash-plotly-env ./workenv
    }
    "enter" {
        docker run -it -v $(pwd):/home/lab/workdir --net=host --name workenv mq37/dash-plotly-env
    }
    "clean" {
        docker rm workenv
        docker rmi mq37/dash-plotly-env
    }
}

