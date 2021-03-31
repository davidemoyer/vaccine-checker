import smtplib
import time

from selenium import webdriver


def check_cvs():
    try:
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.headless = True

        # Change path to local chrome driver
        browser = webdriver.Chrome(options=chromeOptions,
                                   executable_path='<<Insert absolute path to chromedriver.exe file here>>')

        already_sent_availability = {}

        while True:
            browser.get('https://www.cvs.com/immunizations/covid-19-vaccine')

            # Enter the state to be checked below
            connecticut_covid_button = browser.find_element_by_link_text('Connecticut')
            connecticut_covid_button.click()
            cityValues = [x.text for x in browser.find_elements_by_class_name('city')]
            statusValues = [x.text for x in browser.find_elements_by_class_name('status')]

            availability_list = dict(zip(cityValues, statusValues))
            print(availability_list)
            new_available_in_dict = {}
            message_to_send = 'According to CVS the vaccine is currently available in: '

            for key, val in availability_list.items():
                if val == 'Available':
                    new_available_in_dict[key] = val
                    message_to_send += key + ', '

            if already_sent_availability != new_available_in_dict:
                send_email(message_to_send)
                already_sent_availability = new_available_in_dict

            print('message to send: ' + message_to_send)
            print('Newly available in: ', new_available_in_dict)

            time.sleep(30)

    except Exception as e:
        check_cvs()
        print("Exception Caught: ", str(e))
    finally:
        try:
            browser.close()
        except:
            pass


def send_email(message):
    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    # Turning on 'less secure apps' settings as mailbox user
    #
    # Go to your Google Account.
    # On the left navigation panel, click Security.
    # On the bottom of the page, in the Less secure app access panel, click Turn on access.
    # Click the Save button.

    server.login('<<gmail address with less secure apps enabled>>', '<<password goes here>>')

    # AT&T: phonenumber@txt.att.net
    #
    # T-Mobile: phonenumber@tmomail.net
    #
    # Sprint: phonenumber@messaging.sprintpcs.com
    #
    # Verizon: phonenumber@vtext.com or phonenumber@vzwpix.com
    #
    # Virgin Mobile: phonenumber@vmobl.com

    # Send text message through SMS gateway of destination number
    server.sendmail('<<gmail address from above>>', '<<Follow instructions above, example: 8669306480@vtext.com>>',
                    message)


check_cvs()
