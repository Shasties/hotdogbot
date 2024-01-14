import json, boto3, random
from nacl.signing import VerifyKey

PUBLIC_KEY = ''

def lambda_handler(event, context):
  print(event)
  try:
    verifyMessage(event)
  except Exception as e:
    print(e)
    return {
      'statusCode': 401,
      'body': json.dumps('invalid request signature')
    }
  body = json.loads(event['body'])
  t = body['type']

  if t == 1:
    return {
      'statusCode': 200,
      'body': json.dumps({
        'type': 1
      })
    }
  elif t == 2:
    try:
      WriteToSNS(body)
      return {
        'statusCode': 200,
        'body': json.dumps({
          'type': 4,
          'data': {
            'content': "Hot diggety dog! Your order is being processed..."
          }
        })
      }
    except Exception as e:
      print(e)
      return {
        'statusCode': 200,
        'body': json.dumps({
          'type': 4,
          'data': {
            'content': "Uh oh! Something is broken!"
          }
        })
      }
      
  else:
    return {
      'statusCode': 400,
      'body': json.dumps('unhandled request type')
    }

def verifyMessage(event):
  signature = event['headers']['x-signature-ed25519']
  timestamp = event['headers']['x-signature-timestamp']
  body = event['body']
  verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
  try:
    verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
  except Exception as e:
    raise e

def WriteToSNS(body):
  client = boto3.client('sns')
  msg = {"userID":body['member']['user']['id'],"action":"hotdog","uname":body['member']['user']['global_name']}
  msg = json.dumps(msg)
  try:
    resp = client.publish(TargetArn='',Message=msg,MessageGroupId="1",MessageDeduplicationId=str(random.random()))
    print(resp)
  except Exception as e:
    raise e
