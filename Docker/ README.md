docker build -t quote-generator:v1.0 .

docker save -o image.tar quote-generator

docker run quote-generator:v1.0
