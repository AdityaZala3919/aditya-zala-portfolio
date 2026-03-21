"""
Email sending service using SMTP (Gmail)
Handles sending emails from the portfolio contact form.
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
import threading


class EmailService:
    """Service for sending emails via SMTP."""
    
    def __init__(self):
        """Initialize email service with SMTP credentials from environment."""
        self.email_user = os.getenv("EMAIL_USER")
        self.email_pass = os.getenv("EMAIL_PASS")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_contact_email(
        self,
        sender_name: str,
        sender_email: str,
        sender_subject: str,
        sender_message: str,
    ) -> Tuple[bool, str]:
        """
        Send a contact form email to the portfolio owner.
        
        Args:
            sender_name: Name of the person sending the message
            sender_email: Email address of the sender
            sender_subject: Subject from sender
            sender_message: The message content
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Validate credentials are configured
            if not self.email_user or not self.email_pass:
                return False, "Email service not properly configured"
            
            # Create email message
            msg = MIMEMultipart()
            msg["From"] = self.email_user
            msg["To"] = self.email_user
            msg["Subject"] = f"Portfolio Contact: {sender_name}"
            msg["Reply-To"] = sender_email
            
            # Create email body
            body = f"""
Sender Name: {sender_name}

Sender Email: {sender_email}

Sender Subject: {sender_subject}

Sender Body:
{sender_message}

---
This email was sent from your portfolio contact form.
            """
            
            msg.attach(MIMEText(body, "plain"))
            
            # Send email via SMTP with timeout
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
            
            return True, "Email sent successfully"
        
        except smtplib.SMTPAuthenticationError as e:
            return False, f"Authentication failed: {str(e)}"
        except smtplib.SMTPException as e:
            return False, f"SMTP error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"


# Create a singleton instance
email_service = EmailService()
