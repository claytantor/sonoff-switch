import schedule
import requests
import sys
import time

devices = {
    'living_room':'192.168.5.59'
}


# def job():
#     print("I'm working...")
#     r = requests.get('http://192.168.5.59/cm?cmnd=Power%20TOGGLE')
#     # /cm?cmnd=Power%20TOGGLE
#     # /cm?cmnd=Power%20off'

def sonoff_on(ip_addr):
    print("turning on {0}".format(ip_addr))
    r = requests.get('http://{0}/cm?cmnd=Power%20on'.format(ip_addr))

def sonoff_off(ip_addr):
    print("turning off {0}".format(ip_addr))
    r = requests.get('http://{0}/cm?cmnd=Power%20off'.format(ip_addr))


def sonoff_on_living_room():
    sonoff_on(devices['living_room'])
def sonoff_off_living_room():
    sonoff_off(devices['living_room'])
    


def main(argv):
    print("starting sonoff scheduler app.")
    schedule.every().day.at("19:15").do(sonoff_on_living_room)
    schedule.every().day.at("23:30").do(sonoff_off_living_room)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1:])