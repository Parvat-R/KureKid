import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_message(to_email: str, otp: str) -> None:
    """
    Send an email with OTP to the specified email address
    
    Args:
        to_email (str): Recipient email address
        otp (str): One-time password to be sent
    """
    # Get email credentials from environment variables
    from_email = os.getenv('EMAIL_ADDRESS')
    from_password = os.getenv('EMAIL_PASSWORD')
    
    if not from_email or not from_password:
        raise ValueError("Email credentials not found in environment variables")

    # Create message
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = 'Your OTP Code'
    
    # Create the body of the message
    body = f'Your OTP code is: {otp}'
    message.attach(MIMEText(body, 'plain'))

    try:
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login to the server
        server.login(from_email, from_password)
        
        # Send email
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        
        # Close the connection
        server.quit()
        
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")


def send_welcome_message(to_email: str, content: str) -> None:
    """
    Send a welcome email to new users
    
    Args:
        to_email (str): Recipient email address
        content (str): Custom welcome message content
    """
    from_email = os.getenv('EMAIL_ADDRESS')
    from_password = os.getenv('EMAIL_PASSWORD')
    
    if not from_email or not from_password:
        raise ValueError("Email credentials not found in environment variables")

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = 'Welcome to KureKid!'
    
    message.attach(MIMEText(content, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
    except Exception as e:
        raise Exception(f"Failed to send welcome email: {str(e)}")

def send_login_notification(to_email: str, content: str) -> None:
    """
    Send a login notification email
    
    Args:
        to_email (str): Recipient email address
        content (str): Login notification details
    """
    from_email = os.getenv('EMAIL_ADDRESS')
    from_password = os.getenv('EMAIL_PASSWORD')
    
    if not from_email or not from_password:
        raise ValueError("Email credentials not found in environment variables")

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = 'New Login Detected'
    
    message.attach(MIMEText(content, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
    except Exception as e:
        raise Exception(f"Failed to send login notification: {str(e)}")

def send_weekly_report(to_email: str, content: str) -> None:
    """
    Send weekly activity report for the kid
    
    Args:
        to_email (str): Recipient email address
        content (str): Weekly report content
    """
    from_email = os.getenv('EMAIL_ADDRESS')
    from_password = os.getenv('EMAIL_PASSWORD')
    
    if not from_email or not from_password:
        raise ValueError("Email credentials not found in environment variables")

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = 'Weekly Activity Report'
    
    message.attach(MIMEText(content, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
    except Exception as e:
        raise Exception(f"Failed to send weekly report: {str(e)}")
