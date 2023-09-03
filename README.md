# Aviation Stack Data Pipeline

A proof of concept AWS and Python data pipeline.

## Overview 
A simple data pipeline pulling real time active flight data by airport from the
[Aviation
Stack](https://aviationstack.com/?utm_source=FirstPromoter&utm_medium=Affiliate&fpr=victor80&gclid=CjwKCAjw3dCnBhBCEiwAVvLcu8hZqEu3epJZwT70wAz3swfsfGCeicpXVMLBv0SnCX4YDSnpdVm7nxoCt6wQAvD_BwE)
API designed for deployment to AWS. 


## Operating Design
On a daily schedule, EventBridge will trigger the aviation_stack_data_pipeline
Lambda.  The lambda will gather authentication credentials from Secrets Manager
and establish a connection to the destination Postgres RDS instance. Via a get
REST request, the lambda then pulls paginated records up to the configured
threshold amount. The pulls run synchronously, stage data, and upload to the
destination on every pull.  A "STATISTICS" table is generated containing
information about every row's load size linked by a UUID. 


## TODOS:
- Build out infrastructure as code using Terraform Install mocker and mock AWS
- API calls in unit tests.  Improve scalability by separating each pull on a
- separate Lambda process Analyze gathered data and provide distribution
- metrics to applicable fields to improve load statistics.
