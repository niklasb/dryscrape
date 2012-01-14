import time
from dryscrape               import Session
from dryscrape.driver.webkit import Driver

#==========================================
# Setup
#==========================================

email    = 'YOUR_USERNAME_HERE@gmail.com'
password = 'YOUR_PASSWORD_HERE'

# set up a web scraping session
sess = Session(driver   = Driver(),
               base_url = 'https://mail.google.com/')

# there are some failing HTTP requests, so we need to enter
# a more error-resistant mode (like real browsers do)
sess.set_error_tolerant(True)

# we don't need images
sess.set_attribute('auto_load_images', False)

# if we wanted, we could also configure a proxy server to use,
# so we can for example use Fiddler to monitor the requests
# performed by this script
#sess.set_proxy('localhost', 8888)

#==========================================
# GMail send a mail to self
#==========================================

# visit homepage and log in
print "Logging in..."
sess.visit('/')

email_field    = sess.at_css('#Email')
password_field = sess.at_css('#Passwd')
email_field.set(email)
password_field.set(password)

email_field.form().submit()

# find the COMPOSE button and click it
print "Sending a mail..."
compose = sess.at_xpath('//*[contains(text(), "COMPOSE")]')
compose.click()

# compose the mail
to      = sess.at_xpath('//*[@name="to"]', timeout=10)
subject = sess.at_xpath('//*[@name="subject"]')
body    = sess.at_xpath('//*[@name="body"]')

to.set(email)
subject.set("Note to self")
body.set("Don't eat too much bananas")

# send the mail
send = sess.at_xpath('//*[normalize-space(text()) = "Send"]')
send.click()

# open the mail
print "Reading the mail..."
mail = sess.at_xpath('//*[normalize-space(text()) = "Note to self"]', timeout=10)
mail.click()

# sleep a bit to leave the mail a chance to open.
# This is ugly, it would be better to find something
# on the resulting page that we can wait for
time.sleep(3)

# save a screenshot of the web page
print "Writing screenshot to 'gmail.png'"
sess.render('gmail.png')
