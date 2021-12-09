
from amcrest.http import Http
import os
import requests

PUSHOVER_POST_URL = 'https://api.pushover.net/1/messages.json'

def lines(ret):
    line = ''
    for char in ret.iter_content(decode_unicode=True):
        line = line + char
        if line.endswith('\r\n'):
            yield line.strip()
            line = ''


def main():
    with open('build', 'r') as f:
        print(f.read())
    pushover_token =  os.getenv('PUSHOVER_TOKEN')
    pushover_group = os.getenv('PUSHOVER_GROUP')

    host = os.getenv('DOORBELL_HOST')
    port = os.getenv('DOORBELL_PORT', '80')
    user = os.getenv('DOORBELL_USER', 'admin')
    pswd = os.getenv('DOORBELL_PWD')
    msg = os.getenv('PUSH_MESSAGE', 'Someone is at the Front Door')

    relay_url = os.getenv('RELAY_URL', '')
    pushover_payload = {
        'token': pushover_token,
        'user': pushover_group,
        'message': msg
    }
    relay_payload = {
        'command': msg,
        'user': 'kluuvto',
        'broadcast': True
    }
    cam = Http(host, port, user, pswd, retries_connection=5, timeout_protocol=3.05)
    print("Connected")
    ret = cam.command(
        'eventManager.cgi?action=attach&codes=[_DoTalkAction_]',
        timeout_cmd=(3.05, None), stream=True)
    ret.encoding = 'utf-8'

    try:
        for line in lines(ret):
            if "Invite" in line:
                print("Doorbell Event Received")
                requests.post(PUSHOVER_POST_URL, data = pushover_payload)
                if relay_url != '':
                    requests.post(relay_url, data = relay_payload)

    except KeyboardInterrupt:
        ret.close()
        print(' Done!')

if __name__ == '__main__':
    main()