
import json,boto3,random,requests,os

rnames = [
    "I. C. Wiener"
    ]

def lambda_handler(event, context):
    webhook_url = os.getenv("WEBHOOK_URL")
    parsed_message = []
    print(event)
    t = hotdog().replace(" ","%20")
    dicord_data = {
            'username': 'AWS',
            'avatar_url': 'https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png',
            'content': f"Ayyyy, we got a mobile order for uhhh {random.choice(rnames)}",
            "embeds": [{'image':{'url':t}}]
        }

    headers = {'content-type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(dicord_data),
                             headers=headers)

    print(f'Discord response: {response.status_code}')
    print(response.content)

# Return random hotdog pic
def hotdog():
    s3 = boto3.resource('s3')
    buck = os.getenv("S3_BUCKET")
    cf = os.getenv("CLOUDFRONT")
    my_bucket = s3.Bucket(buck)
    o = list(my_bucket.objects.all())
    r_file = random.choice(o)
    while r_file.key == "hotdogs/":
      r_file = random.choice(o)
    return f"{cf}{r_file.key}"
