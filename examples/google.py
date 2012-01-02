import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                '../lib'))
import webkit_scraping

if __name__ == '__main__':
  # set up a web scraping session
  driver = webkit_scraping.webkit_server.Driver()
  sess = webkit_scraping.scraping.Session(driver = driver,
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
