# S3 buckets
# IAM
# Lambda
# Step Functions
- build visual pipelines
# CloudWatch
- alarms
- logs
- metrics
- events
- serviceLens
- x-ray
# Cloudformation
tool to rule AWS services via config file not GUI
Terraform, AWS SAM, serverless, CDK are built on top of it
# CDK
AWS API (python, javascript) that help to deploy application
# App Runner
# SQS

Can be done in channels
At least Once delivery

cross account publishin/processing is possible
messages are limited to 256 KiB
## Dead Letter Queues
Queue for failed messages
can be configured to move messages there automatically after number of tries

## Standart queue
order does not guaranteed (infinitive througput)
## FIFO
transactions per second limit (more expencive)

# SNS - Simple Notification Service
Message publishing and processing service

topics - can copies messages to different queues
