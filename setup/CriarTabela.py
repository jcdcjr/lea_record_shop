import boto3


def criar_tabela(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
        # local dynamodb = boto3.resource('dynamodb', http://localhost:8000")

    table = dynamodb.create_table(
        TableName='LeaRecordShop',
        KeySchema=[
            {
                'AttributeName': 'pk',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'sk',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'pk',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'sk',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'data',
                'AttributeType': 'S'
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'gsi_1',
                'KeySchema': [
                    {
                        'AttributeName': 'sk',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'data',
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                }
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table


if __name__ == '__main__':
    lea_shop_tabela = criar_tabela()
    print("status:", lea_shop_tabela.table_status)