import dryscrape
import sys

if 'linux' in sys.platform:
    # start xvfb in case no X is running. Make sure xvfb 
    # is installed, otherwise this won't work!
    dryscrape.start_xvfb()

search_term = 'dryscrape'

# set up a web scraping session
sess = dryscrape.Session(base_url = 'http://google.com')

# we don't need images
sess.set_attribute('auto_load_images', False)

# visit homepage and search for a term
sess.visit('/')
q = sess.at_xpath('//*[@name="q"]')
q.set(search_term)
q.form().submit()

# extract all links
for link in sess.xpath('//a[@href]'):
  print(link['href'])

# save a screenshot of the web page
sess.render('google.png')
print("Screenshot written to 'google.png'")
