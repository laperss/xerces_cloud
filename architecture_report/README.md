# architecture of the application

The service will work like the AWS lambda service, where images are resized.

![AWS Lambda](Lambda_FileProcessing.png)

# Components

* A workload generator
* A RabbitMQ server: queue between workload generator and the services
* Service node: convert video and return the result to the MQ server
* A monitor to track the CPU utilization?

# Exposed interfaces

# Technology stack

# How will the application be scale-able?

# Robustness


# Requirements

* The service MUST take input videos and convert them to an output video.
* The service MUST be ​**salable**.
* The service MUST be ​**robust​**.
* The workload generator MUST submit video conversion requests to the service and measure values such as response time 1 and queue length.
