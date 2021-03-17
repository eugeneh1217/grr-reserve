import argparse
import schedule
import datetime
import time

from reserve import Reserver

DEFAULT_CHROME_VERSION = 89

DAY_TO_NUM = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6,
}

CYCLE = 60 * 30

front = 1

def next_day(day: int):
    today = datetime.datetime.today()
    days_ahead = (day - today.weekday()) % 7
    return (today + datetime.timedelta(days=days_ahead)).day

def book_on(chrome_version: int, day: int):
    global front
    front *= -1
    reserver = Reserver(chrome_version)
    reserver.book(
        'front' if front == 1 else 'back',
        next_day(day),
        '6 PM',
        'eugeneh1217@gmail.com'
    )

def get_args(*args):
    parser = argparse.ArgumentParser(description='Book time slots for grr in accordance to schedule.')
    parser.add_argument(
        '--chrome-version', '-v',
        metavar='V',
        type=int,
        help='Version of chrome being used, defaults to 89.'
    )
    args = parser.parse_args()
    if args.chrome_version is None:
        args.chrome_version = DEFAULT_CHROME_VERSION
    return args

def schedule_bookings(chrome_version: int, time: str):
    schedule.every().sunday.at(time).do(book_on, chrome_version, DAY_TO_NUM['thursday'])
    schedule.every().wednesday.at(time).do(book_on, chrome_version, DAY_TO_NUM['sunday'])
    schedule.every().friday.at(time).do(book_on, chrome_version, DAY_TO_NUM['tuesday'])

def main(*args):
    args = get_args(args)
    schedule_bookings(args.chrome_version, '18:00')
    print(f"Bot started at: {datetime.datetime.now().strftime('%H:%M:%S')}")
    while True:
        schedule.run_pending()
        time.sleep(CYCLE)

if __name__ == '__main__':
    main()
