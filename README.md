# Aviation Stack Data Pipeline

version 0.0.1
A proof of concept AWS and Python data pipeline.

## Overview 
A simple data pipeline pulling real time active flight data by airport from the
[Aviation
Stack](https://aviationstack.com/?utm_source=FirstPromoter&utm_medium=Affiliate&fpr=victor80&gclid=CjwKCAjw3dCnBhBCEiwAVvLcu8hZqEu3epJZwT70wAz3swfsfGCeicpXVMLBv0SnCX4YDSnpdVm7nxoCt6wQAvD_BwE)
API designed for deployment to AWS. This pipeline is a use-case concept to
evaluate using the Aviation Stack API when rendering aircraft in flight in
flight simulators for recreation or pilot training. 


## Operating Design
On a daily schedule, EventBridge will trigger the aviation_stack_data_pipeline
Lambda. The lambda will gather authentication credentials from Secrets Manager
and establish a connection to the destination Postgres RDS instance. A
configuration file named "config.toml" in a "LOAD_CONFIG" S3 bucket will be
gathered and parsed to select which airport ICAO's will be gathered. Each
airport ICAO will contain it's own table as a simple strategy for a healthy
partitioning of large data. Via a get REST request, the lambda then pulls
paginated records up to the configured threshold amount. The pulls run
synchronously, stage data, and upload to the destination on every pull.  A
"STATISTICS" table is generated containing information about every row's load
size linked by a UUID. 


## Usage Warnings
- All tests and build scripts have been run on a Linux operating system using
	Bash. (Ubuntu 22.04.3) 
- On the free tier of Aviation Stack, this pipeline will
	quickly consume the monthly request limit if not throttled. 



## TODOS:
- Build out infrastructure as code using Terraform Install mocker and mock AWS
	API calls in unit tests.  
- Improve scalability by separating each pull on a Separate Lambda process Analyze gathered data and provide distribution
  Metrics to applicable fields to improve load statistics.
- Replace constant string literals with configurable environment variables.
