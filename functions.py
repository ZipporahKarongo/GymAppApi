import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(receiver_email, subject, main_content):
    # main_content = '''SAMPLE Message'''
    sender_email = "karzippy@gmail.com"
    sender_pass = "18borninjanuary"
    #  receiver_email = receiver_email

    # set up MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['to'] = receiver_email
    message['Subject'] = subject

    # crate the body
    message.attach(MIMEText(main_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_email, sender_pass)
    text = message.as_string()

    try:
        session.sendmail(sender_email, receiver_email, text)
        session.quit()
    except:
        print('Error')


# send_email("zipporahkarongo@gmail.com", "h", "hello")

import africastalking


def send_sms(phone, message):
    username = 'joe2022'
    api_key = '15d1fb388bcb3cb033f75b7fffcb9d0b45ff71352a9bed062487b99c0b5ce670'
    africastalking.initialize(username, api_key)

    recipients = [phone]
    # message = "Hey AT Ninja!"
    sender = "AFRICASTKNG"

    try:
        sms = africastalking.SMS
        response = sms.send(message, recipients)
        print(response)
    except:
        print("sms not sent")


# send_sms("+254722843541", "Hi Siz!")


import hashlib, binascii, os


# This function receives a password as a parameter
# its hashes and salts using sha512 encoding
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    # print('Salt', salt)
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


# below provide a plain password and see its hashed/salted output
# hashedpassword = hash_password("mypassword123")
# print(hashedpassword)
# #

# this function checks if hashed password is the same as
# provided password
def verify_password(hashed_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = hashed_password[:64]
    hashed_password = hashed_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)

    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == hashed_password


def verify_password2(password_given, password_has):
    return password_given == password_has


# run it , provide the hashed and the real password
# SHOULD GIVE YOU TRUE/FALSE
# hashedpassword = "b8d38c88da29e4488a2027351ee3068b8b5fabb7a82f38e9c5cbc2f9ac96e1ecb2fce3dfc0331763e80778ee4dc9a7699f13bee27cf829f877b3ec2326c98160dba773ab54c6087117d620739cd20a17a90f41ad1de66008929956300caead5a"
# status = verify_password(hashedpassword, "mypassword123")
# print(status)

import random, string


def otp_gen():
    length = 6
    # def data
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    # all combined

    all = lower + upper + num

    # generate then in random 6

    otp = random.sample(all, length)
    # join the list

    final_otp = "".join(otp)
    return (final_otp)
