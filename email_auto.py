import os
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

#CONFIG
os.environ["GEMINI_API_KEY"] = ""  # or export GEMINI_API_KEY externally
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

IMAP_SERVER = 'imap.gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
EMAIL_ACCOUNT = 'abc'
EMAIL_PASSWORD = 'abc'

#AI Function
def generate_gemini_reply(prompt_text):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt_text)
    return response.text

#Email Processor
def check_and_reply():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select('inbox')
    status, data = mail.search(None, '(UNSEEN)')
    for num in data[0].split():
        status, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        sender = email.utils.parseaddr(msg['From'])[1]
        subject = msg['Subject']
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")
        reply_text = generate_gemini_reply(body)
        reply_msg = MIMEMultipart()
        reply_msg['From'] = EMAIL_ACCOUNT
        reply_msg['To'] = sender
        reply_msg['Subject'] = 'Re: ' + subject
        reply_msg.attach(MIMEText(reply_text, 'plain'))
        smtp = smtplib.SMTP(SMTP_SERVER, 587)
        smtp.starttls()
        smtp.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        smtp.send_message(reply_msg)
        smtp.quit()
    mail.close(); mail.logout()

if __name__ == "__main__":
    check_and_reply()
