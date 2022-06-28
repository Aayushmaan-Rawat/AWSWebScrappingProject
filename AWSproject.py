import env
import requests
import json
import boto3
from datetime import datetime
import time
print('hello')
URL = 'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=&postalCode=M5G2C3&skus=15507363'

headers = {
	'authority': 'www.bestbuy.ca',
	'pragma': 'no-cache',
	'cache-control': 'no-cache',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
	'accept': '*/*',
	'sec-fetch-site': 'same-origin',
	'sec-fetch-mode': 'cors',
	'sec-fetch-dest': 'empty',
	'referer': 'https://www.bestbuy.ca/en-ca/product/zotac-nvidia-geforce-rtx-3080-ti-amp-holo-12gb-gddr6x-video-card/15507363',
	'accept-language': 'en-US,en;q=0.9'
}
def main():
    quantity = 0
    attempt = 0
    print("hello")

    while (quantity < 1):  # this loop runs until the quantity is greater than 1 for the very 1st time.
        response = requests.get(URL,headers=headers)
        response_formatted = json.loads(response.content.decode('utf-8-sig').encode('utf-8'))

        quantity = response_formatted['availabilities'][0]['shipping']['quantityRemaining']

        if (quantity < 1):
            #Out Of stock
            print('Time=' + str(datetime.now()) + "- Attempt=" + str(attempt))
            attempt += 1
            time.sleep(5)
        else:
            print('Hey its in stock! Quantity=' + str(quantity))
            publish(quantity)


def publish(quantity):
    arn = 'arn:aws:sns:us-east-1:206070559467:InStockTopic'
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=env.accessKey,
        aws_secret_access_key=env.secretKey,
        region_name='us-east-1'
    )

    response = sns_client.publish(TopicArn=arn, Message='Its in stock! Quantity=' + str(quantity))
    print(response)

main()