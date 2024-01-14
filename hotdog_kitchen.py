
import json,boto3,random,requests,os

def lambda_handler(event, context):
    webhook_url = os.getenv("WEBHOOK_URL")
    parsed_message = []
    print(event)
    for record in event.get('Records', []):
        sns_message = json.loads(record['body'])
        t = hotdog().replace(" ","%20")

        discord_data = {}
        if canEat(sns_message['userID']):
            dicord_data = {
                'username': 'AWS',
                'avatar_url': 'https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png',
                'content': f"Here's that hotdog you ordered, {sns_message['uname']}",
                "embeds": [{'image':{'url':t}}]
            }
        else:
            dicord_data = {
                'username': 'AWS',
                'avatar_url': 'https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png',
                'content': f"oooooo {sns_message['uname']}'s tummy hurts from eating too many hotdogs."
            }

        headers = {'content-type': 'application/json'}
        response = requests.post(webhook_url, data=json.dumps(dicord_data),
                                 headers=headers)

        print(f'Discord response: {response.status_code}')
        print(response.content)

# Return random hotdog pic
def hotdog():
    buk = os.getenv("S3_BUCKET")
    cf = os.getenv("CLOUDFRONT")

    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(buk)
    o = list(my_bucket.objects.all())
    r_file = random.choice(o)
    while r_file.key == "hotdogs/":
      r_file = random.choice(o)
    return f"{cf}{r_file.key}"
     
def canEat(uid):
  dyn_client = boto3.resource('dynamodb')
  table = dyn_client.Table('hotdogs')
  u = table.get_item(Key={'userID': uid})
  if 'Item' not in u.keys():
    initUser(table,uid)
  elif u['Item']['hunger'] >= 0 and u['Item']['hunger'] + 5 <= u['Item']['max_hunger']:
    table.update_item(
      Key = {'userID': uid},
      UpdateExpression = "set #hunger = :h",
      ExpressionAttributeNames = {
        "#hunger": "hunger"
      },
      ExpressionAttributeValues = {
        ":h": u['Item']['hunger']+5
      })
  else:
    return False
  return True

def initUser(tab,uid):
  tab.put_item(
   Item={
        'userID': uid,
        'hunger': 5,
        'max_hunger': 10
    }
)
