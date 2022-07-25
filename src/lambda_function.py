import json
import requests

def lambda_handler(event, context):

    search_engine_url = 'https://www.googleapis.com/customsearch/v1'
    key = 'AIzaSyBN6UgYDlHBf9Fx8E7JGBTZVA4qyZA06rE'
    cx = 'b07c65c3e12e1479e'
    d = dict(x.split("=") for x in event['body'].split("&"))
    search_query = d['text']
    welcome_text = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hello, I'm Jarvis! Your personal assistant bringing search engine to your workspace! \n\n *Search Results:*"
			}
		}
    data = {'key': key, 'cx': cx, 'q': search_query}
    response = requests.get(search_engine_url, params=data)
    search_results = response.json()
    build_block = {}
    build_block['blocks'] = []
    build_block['blocks'].append(welcome_text)
    for result in search_results['items']:
        payload = {'type': 'section'}
        payload['text'] = {}
        payload['text']['type'] = 'mrkdwn'
        payload['text']['text'] = '*{}*\n{}'.format(result['title'], result['snippet'])
        divider = {'type': 'divider'}
        payload['accessory'] = {}
        payload['accessory']['type'] = 'image'
        if result['pagemap'].get('cse_thumbnail'):
            image = result['pagemap']['cse_thumbnail'][0]['src']
        else:
            image = 'https://s3-media2.fl.yelpcdn.com/bphoto/DawwNigKJ2ckPeDeDM7jAg/o.jpg'
        payload['accessory']['image_url'] = image
        payload['accessory']['alt_text'] = 'alt text for image'
        build_block['blocks'].append(divider)
        action = {'type': 'actions'}
        action['elements'] = []
        button = {}
        button['type'] = 'button'
        button['text'] = {}
        button['text']['type'] = 'plain_text'
        button['text']['text'] = 'Read more'
        button['text']['emoji'] = True
        button['value'] = result['link']
        action['elements'].append(button)
        build_block['blocks'].append(payload)
        build_block['blocks'].append(action)
        print(build_block)
    return {
        'statusCode': 200,
        'body': json.dumps(build_block)
    }
