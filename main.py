from bottle import route, run, request, default_app, abort
import xml.etree.ElementTree as XML

secret = 'some_url_safe_secret'

namespaces = {
    'yt': 'http://www.youtube.com/xml/schemas/2015',
    'xmlns': 'http://www.w3.org/2005/Atom'
}


@route('/callback', method='get')
@route('/callback', method='post')
def index():
    print(f'Got a {request.method} request!')
    print()
    if request.method == 'POST':
        response = request.body.read().decode('utf-8')
        root = XML.fromstring(response)

        for entry in root.findall('xmlns:entry', namespaces=namespaces):
            deleted = entry.find('at:deleted-entry')
            if deleted:
                # return
                pass
            video_id = entry.find('yt:videoId', namespaces=namespaces).text
            title = entry.find('xmlns:title', namespaces=namespaces).text
            link = entry.find('xmlns:link', namespaces=namespaces).get('href')
            for el in entry.find(
                    'xmlns:author', namespaces=namespaces):
                if el.tag.split('}')[-1] == 'name':
                    author = el.text

            message = f'{author} just posted a video on youtube!\nCheck this out {link}'
            print(message)

        # Do Something Here

        return 'Goodly'

    try:
        print(request)
        mode = request.query['hub.mode']
        print('\nMode')
        print(mode)
        challenge = request.query['hub.challenge']
        print('\nChallenge')
        print(challenge)
        return challenge
        verify_token = request.query['hub.verify_token']
        print(verify_token)
        print(mode, challenge, verify_token)
    except KeyError:
        print('KeyError, Aborting')
        abort(404)

    if mode == 'subscribe' and verify_token == secret:
        return challenge
    abort(404)
    if request.method == 'GET':
        print('Got GET request')


if __name__ == '__main__':
    """For Development"""
    run(host='0.0.0.0', port=80, debug=True)

# For Production
app = default_app()
