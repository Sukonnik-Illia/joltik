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
Messages can be sent to:
- HTTP post request
- email and email-JSON
- SQS
- SMS - only registered phone numbers
## topics
Can copies messages to different queues
## Subscriptions

# DynamoDB
document storage

# Aurora
AWS SQL engine (MySQL or PostgreSQL compatible)

# Cognito
Auth and Authorize service
# Aplify

# ECS - Elasctic Container Service
Something like Kubernetes but amazon locked, easier to start with but not so portable
# EKS - Elastic Kubertetes Service

# Secrets Manager

# EC2 - Elastic Compute Cloud
Just virtual machine

# API Gateway

# DBs
- RDS Relational Database Service with different engines. Aws just manages backups and scaling for you
- DocumentDB - Managed MongoDB
- DynamoDB - Key value lookups
- Opensearch - AWS version of Elasticsearch

# Cache
- ElastiCache - Memcache/Redis version
- CloudFront - Caching resorses (S3 and something elese)

# Kinesis
Massive events (like user hovering on something or clicks)

# Step Functions
