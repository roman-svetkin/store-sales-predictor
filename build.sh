#!/bin/bash
# If the following command gives a "Unknown options: --no-include-email"
# error then the local version of AWSCLI needs to be upgraded
# http://docs.aws.amazon.com/cli/latest/userguide/awscli-install-bundle.html
# At time of writing `aws --version` returns `aws-cli/1.11.99` for me

VERSION=0.0.1

awsversion=$(aws --version | cut -d '/' -f 2 | cut -d '.' -f 1)

# Login to Amazon Elastic Container Registry
if [ "$awsversion" = "1" ]
then
    echo "awscli V1"
    eval $(aws ecr get-login --no-include-email --region YOUR_AWS_REGION)
elif [ "$awsversion" = "2" ]
then
    echo "awscli V2"
    aws ecr get-login-password --region YOUR_AWS_REGION | docker login --password-stdin --username AWS https://YOUR_AWS_ACCOUNT.dkr.ecr.YOUR_AWS_REGION.amazonaws.com
else
    echo "Unknown AWS version above 2.x: $awsversion"
    exit
fi

# Install linting and unit test dependencies
pip install --upgrade isort pylint black pytest pre-commit
pre-commit install

# Run linting and unit tests

pylint --recursive=y --rcfile=pyproject.toml .
black --config=pyproject.toml .
isort --settings-path=pyproject.toml .
pytest -v

# Push commands as advised by ECS 'View Push Commands' option on AWS ECS repository web site
docker buildx build --platform linux/amd64 --push -t YOUR_AWS_ACCOUNT.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/loan-rate-predictor:$VERSION .

# docker run --rm -p:8080:8080 --name loan-rate-predictor --env TIKTOK_ACCESS_TOKEN=xxxxx --env TIKTOK_ADVERTISER_ID=xxxxx  YOUR_AWS_ACCOUNT.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/loan-rate-predictor:0.0.1
