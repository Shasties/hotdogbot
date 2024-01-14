import boto3

def lambda_handler(event, context):
    dyn_client = boto3.resource('dynamodb')
    table = dyn_client.Table('hotdogs')
    os = table.scan()
    print(os)
    for o in os["Items"]:
      if o["hunger"] > 0:
        table.update_item(
          Key = {'userID': o['userID']},
          UpdateExpression = "set #hunger = :h",
          ExpressionAttributeNames = {
            "#hunger": "hunger"
          },
          ExpressionAttributeValues = {
            ":h": o['hunger'] - 1
          })
