# uses mechanize to post command line args
# to fug/toaster, message required, usage:
# python toast.py 'secret message' -v 5 -t 36
# uses std defaults of 1 view, 20 hours
import mechanize, sys, argparse

URL = 'https://fugacious.18f.gov/'

# set command line arg flags
parser = argparse.ArgumentParser()
parser.add_argument('message')
parser.add_argument('-v', '--views', help='num of views to expire')
parser.add_argument('-t', '--time', help='hours to expire')

args = parser.parse_args()

# sets encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf8')

# opens mechanize session, ignores robits
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(URL)

# selects form on page
def select_form(form):
  return form.attrs.get('id', None) == 'new_message'

br.select_form(predicate=select_form)

# fills in form with mandatory arg (message) and
# looks for optional args
br.form['message[body]'] = args.message

if args.views:
  br.form['message[max_views]'] = args.views

if args.time:
  br.form['message[hours]'] = args.time

# submits + prints secret url
br.submit()
toast_url = br.geturl()

print toast_url
