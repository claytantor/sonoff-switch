import schedule
import requests
import sys, os
import time
import argparse
import yaml

from flashlexiot.sdk import FlashlexSDK


def flashlex_job(config):

    lookup = {
        "on": "Power%20on",
        "off": "Power%20off",
        "toggle": "Power%20TOGGLE"
    }

    sdk = FlashlexSDK(config)
    records = sdk.getSubscribedMessages()

    # process new messages
    for record in records:
        #print("record", record)
        #print("payload message", record['message']['payload']['message'])

        payload_message = record['message']['payload']['message']

        ## find the ip address
        result = list(filter(lambda x: (x['name'] == payload_message['device']), config['devices']))

        
        for device in result:
            ## find the command
            r = requests.get('http://{0}/cm?cmnd={1}'.format(device['ip'], lookup[payload_message['value']]))

        sdk.removeMessageFromStore(record)


def sonoff_job(ip_addr, sonoff_command):
    print("setting {0} to {1}".format(ip_addr, sonoff_command))
    r = requests.get('http://{0}/cm?cmnd={1}'.format(ip_addr, sonoff_command))
    
def loadConfig(configFile):
    cfg = None
    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg

def main(argv):
    print("starting sonoff app.")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", action="store", 
        required=True, dest="config", help="the YAML configuration file")

    args = parser.parse_args()
    config = loadConfig(args.config)

    #schedule flashlex to accept commands 
    schedule.every(10).seconds.do(flashlex_job, config=config)

    print("starting sonoff scheduler app.")
    for device in config['devices']: 
        #print(device)
        for schedule_item in device['schedule']:
            schedule.every().day.at(schedule_item['time']).do(sonoff_job, 
                ip_addr=device['ip'], sonoff_command=schedule_item['command'])
    

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1:])
