#!/usr/bin/env python
# Tested by Tom on Python 2.7.5 and Python 3.3.1 running on Arch Linux
import json
import datetime
from requests import get
from optparse import OptionParser

def load_options():
    parser = OptionParser()
    parser.add_option("-t", "--tweet", dest="tweet", default=False,
                  help="Whether or not to tweet results for test", metavar="FILE")
    (options, args) = parser.parse_args()
    return options

def date_pair(date_date):
    return {
        'days': (datetime.date.today() - date_date).days,
        'date': date_date.strftime('%A, %B %d, %Y'),
    }

def observed_data():
    url = 'https://premium.scraperwiki.com/cc7znvq/47d80ae900e04f2/sql'
    sql = '''SELECT max(date) FROM t1;'''

    r = get(url, params = {'q': sql})
    date_string = json.loads(r.text)[0]['max(date)']
    date_date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()

    return date_pair(date_date)

def expected_data():
    'The date when the script should have last run'
    adate = datetime.date.today()
    adate -= datetime.timedelta(days=1)
    while adate.weekday() >= 4: # Mon-Fri are 0-4
        adate -= datetime.timedelta(days=1)
    return date_pair(adate)

@treasuryio.tweet
def gen_test_message():
    peeps = "@brianabelson @mhkeller @jbialer @thomaslevine @bdewilde @Cezary"
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    observed = observed_data()
    expected = expected_data()

    if observed['days'] > 7:
        return "The parser last ran on %s. Something is definitely wrong!" % observed['date']

    elif observed['date'] < expected['date']:
        return "Unless %s is a holiday, something is up!" % expected['date']
    else:
        return "All seems well!"

@treasuryio.tweet
def gen_test_tweet(tweet=True):
    peeps = "@brianabelson @mhkeller @jbialer @thomaslevine @bdewilde @Cezary"
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    observed = observed_data()
    expected = expected_data()

    if observed['days'] > 7:
        if tweet:
            return "Yo %s! Something is definitely wrong! - %s" % (peeps, current_date)
        else:
            return "The parser last ran on %s. Something is definitely wrong!" % observed['date']

    elif observed['date'] < expected['date']:
        if tweet:
            return "Hey %s, somethings wrong if %s is a holiday! - %s" % (peeps, expected['date'])
        else:
            return "Unless %s is a holiday, something is up!" % expected['date']
    else:
        if tweet:
            return None
        else:
            return "All seems well!"

if __name__ == '__main__':
    options = load_options()
    print gen_message(tweet=False)