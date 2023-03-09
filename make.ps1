$1 = $args[0]

switch ($1)
{
    "build" {
        docker build -t mq37/dash-plotly-env ./workenv
    }
    "enter" {
        docker run -it -v ${PWD}:/home/lab/workdir -p 8050:8050 --name workenv mq37/dash-plotly-env
    }
    "clean" {
        docker rm workenv
        docker rmi mq37/dash-plotly-env
    }
}

