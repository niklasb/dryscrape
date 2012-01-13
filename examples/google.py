from dryscrape               import Session
from dryscrape.driver.webkit import Driver

search_term = 'dryscrape'

# set up a web scraping session
sess = Session(driver   = Driver(),
               base_url = 'http://google.com')

# we don't need images
sess.set_attribute('auto_load_images', False)

# visit homepage and search for a term
sess.visit('/')
q = sess.at_xpath('//*[@name="q"]')
q.set(search_term)
q.form().submit()

# save a screenshot of the web page
sess.render('google.png')
print "Screenshot written to 'google.png'"
