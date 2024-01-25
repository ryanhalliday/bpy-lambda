import os
import json
import bpy
import boto3


def lambda_handler(event, context):
    """Blender bpy Lambda function

    Parameters
    ----------
    event: dict, required
        SQS Input or API Gateway Lambda Proxy Input Format

        SQS Event doc: https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html#example-standard-queue-message-event
        API Gateway Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format or None: dict or None

        API Gateway return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # Example SQS message. They come in batches.
    # for record in event['Records']:
    #     data = json.loads(record['body'])
    #     # Process your message here.

    # Example downloading from S3
    # s3 = boto3.client('s3')
    # s3.download_file(os.getenv('S3_BUCKET'), 'WaterBottle.glb', '/tmp/WaterBottle.glb')
    # bpy.ops.import_scene.gltf(filepath="/tmp/WaterBottle.glb")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": bpy.app.version_string,
                # "vert_count": len(bpy.context.object.data.vertices)
            }
        ),
    }
