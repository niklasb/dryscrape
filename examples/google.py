import os, sys

from pyscrape               import Session
from pyscrape.driver.webkit import Driver

if __name__ == '__main__':
  # set up a web scraping session
  sess = Session(driver   = Driver(),
                 base_url = 'http://google.com')

  # we don't need images
  sess.set_attribute('auto_load_images', False)

  # visit homepage and search for a term
  sess.visit('/')
  q = sess.at_xpath('//*[@name="q"]')
  q.set(sys.argv[1])
  q.form().submit()

  # save a screenshot of the web page
  sess.render('google.png')
  print "Screenshot written to 'google.png'"
