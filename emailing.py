import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

# Opens the hidden .env file variables and loads it into memory.
load_dotenv()

# Securely grab all credentials without exposing them in the code
# os.getenv() safely pulls your private data from memory instead of the code
PASSWORD = os.getenv("PASSWORD")
SENDER = os.getenv("SENDER_EMAIL")
RECEIVER = os.getenv("RECEIVER_EMAIL")


# building the email
def send_email(image_path):
    print("send_email function started")
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    # handling the image
    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype="png")

    # Sending it through the Internet
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()

    # Authentication and delivery
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email function ended!!!")
    print("Email sent successfully!")


# -----------------------------------------
if __name__ == "__main__":
    send_email(image_path="images/16.png")
