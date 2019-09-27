import schedule
import requests
import sys, os
import time
import argparse
import yaml

# def job():
#     print("I'm working...")
#     r = requests.get('http://192.168.5.59/cm?cmnd=Power%20TOGGLE')
#     # /cm?cmnd=Power%20TOGGLE
#     # /cm?cmnd=Power%20off'
#     # /cm?cmnd=Power%20on'

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

    print("starting sonoff scheduler app.")
    lr = config['devices']['living-room']
    for schedule_item in lr['schedule']:
        print(schedule_item)
        schedule.every().day.at(schedule_item['time']).do(sonoff_job, 
            ip_addr=config['devices']['living-room']['ip'], sonoff_command=schedule_item['command'])

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1:])