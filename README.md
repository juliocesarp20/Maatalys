# Maatalys
Maatalys is an API built to serve as the backbone for an investigation application focused on analyzing public spending. It provides the necessary infrastructure and tools for users to manage investigations and searches

## Tech
- Python
- FastAPI
- PostgreSQL
- Apache Kafka
- Docker
- Terraform

## Deploy
AWS ECS using Application Load Balancer (Note: For development purposes 2 public subnets are being used, see the diagram below.). Missing Route 53 and MSK

![Sem título-2025-06-02-0242](https://github.com/user-attachments/assets/20df5f1e-4fbf-41b6-8326-36a37916820e)

## TODO

- [ ] Remove AWS tokens
- [ ] Clean bad comments
- [ ] Update private/public subnet
- [ ] Deploy MSK
- [ ] Add logic to send processed searches to the automation project using Kafka
- [ ] Separate search/investigation processing logic for better scalability
- [ ] Add integration tests
- [ ] Add unit tests
- [ ] Add refresh token for JWT






