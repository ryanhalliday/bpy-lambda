# bpy-lambda

This is a template to run Blender `bpy` scripts on AWS Lambda. 

You can make it run with SQS messages (_recommended_) or HTTP calls via API Gateway.

This uses AWS SAM for deployment and configuration so you should [Install](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) that and all it's requirements (aws cli/docker/python3).

**Current Blender version: 3.6**

You can find more instructions and examples on using it on [my blog](https://blog.ryanhalliday.com/2024/02/blender-bpy-on-aws-lambda.html).

## How to use

Download this repository or use as a [Github Template](https://github.com/new?template_name=bpy-lambda&template_owner=ry167).

Edit `bpy_lambda/app.py` ensuring your code runs from the `lambda_handler(event, context)` function

This is a pretty basic AWS SAM setup, so go read the instructions on how to use that for the most part. 

_**Mac OS / M1 / M2 Note:** This probably won't work due to QEMU / Docker bugs. Spin up a VM or remote server and do all the build steps there._

```bash
# Build the docker container
sam build

# Invoke the lambda locally, no arguments
sam local invoke

# Invoke the lambda locally with a SQS event
sam local invoke BpyLambdaFunction --event events/sqs-receive-message.json

# Deploy the container to AWS
sam deploy --guided

# See logs
sam logs -n BpyLambdaFunction --stack-name "bpy-lambda" --tail

####
## Other misc command examples
####

# Run as a local HTTP API
sam local start-api

# If you want to delete what you deployed in testing, change the name if it was different
sam delete --stack-name "bpy-lambda"
```

## Changing Memory and Disk

The default is 1024 MB memory and 512 MB disk.

In `template.yaml`:
- Edit `MemorySize` for memory allocation
- Edit `EphemeralStorage.Size` for disk size

Note: memory allocation is what increases CPU speed in Lambda, so you may end up paying more per second but needing less seconds by going for more memory. 


### Account limits
- If you are using a new AWS account you likely will only have 3008 MB as your max memory.
- If you have a used AWS account the limit is likely increased to 10240 MB.


## Accessing existing S3 buckets

If you are looking at this you probably have all of your 3D models in S3. But the bucket already exists so you can't create it as part of the SAM / Cloudformation stack.

Uncomment the following sections: 
- `Parameters.S3BucketName`
- `Policies.S3CrudPolicy`
- `Environment.Variables.S3_BUCKET`

When you run `sam deploy --guided` you will be prompted to enter a bucket name. 

Ensure you use `os.getenv('S3_BUCKET')` in your `app.py`.


## Using with API Gateway

I recommend you use SQS, as the jobs you are doing in Blender probably take more than a few seconds and don't make much sense for a request/response style HTTP workflow. 

But if you want to do that, who am I to stop you. Uncomment the `BpyLambdaApi` section in `template.yaml` and the ARN in the `Outputs`


## Changing the Blender version

You can see a list of bpy versions published on PyPI here: https://pypi.org/project/bpy/#history

Change the version string in `Dockerfile` to match the version you want.

`bpy` is installed outside of your `requirements.txt` so that the image doesn't have to be rebuilt as much, but you can shift it there if you prefer.

## BatchSize

The default `BatchSize` is 10 and there is an example line in `template.yaml` to set it to 1.

The timeout for a lambda function is for all batch items, not per item. So if you have long running functions it is definitely a good idea to change this to 1.


## I don't want to use SAM, give me raw Lambda

Pretty much delete everything except `bpy_lambda/`, build it as a container, push it to ECR and then use it as an image for your Lambda. 

Follow the steps under Deploying the Image here: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-clients


## You are stupid and doing it all wrong

AWS can be a lot to deal with. If I did something wrong, please raise an issue and I'll try to fix it.


## TODO 

- [ ] Setup as a cookiecutter so we can use: `sam init -l gh:ry167/bpy-lambda-cookiecutter`
- [ ] [Publish to AWS SAR](https://docs.aws.amazon.com/serverlessrepo/latest/devguide/serverlessrepo-publishing-applications.html)
- [ ] Test out if it is a good idea to mount an EFS volume as a cache for downloaded resources
- [ ] Try it out with layers
- [ ] I also wrote code for `blender-lambda` with SAM. If you want that, send me a message or raise an issue. I like it less than the `bpy` solution though. 
- [ ] Consider compiling `bpy` rather than installing from PyPI


## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

[Blender's Python API](https://docs.blender.org/api/3.6/index.html)

Some container setup commands were taken from [ranchcomputing/blender-cpu-image](https://github.com/ranchcomputing/blender-cpu-image) which was inspired by [nytimes/rd-blender-docker](https://github.com/nytimes/rd-blender-docker). Both are awesome.
