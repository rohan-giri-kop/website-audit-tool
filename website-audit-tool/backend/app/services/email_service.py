"""
=========================================================
AI WEBSITE AUDIT TOOL
EMAIL SERVICE
=========================================================
"""

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.app.utils.config import settings


# =========================================================
# SMTP SETTINGS
# =========================================================

SMTP_HOST = settings.email_host

SMTP_PORT = settings.email_port

SMTP_EMAIL = settings.email_address

SMTP_PASSWORD = settings.email_password

EMAIL_FROM = settings.email_from


# =========================================================
# CREATE SMTP CONNECTION
# =========================================================

def create_smtp_connection():
    """
    Create Gmail SMTP connection.
    """

    server = smtplib.SMTP(

        SMTP_HOST,

        SMTP_PORT

    )

    server.ehlo()

    server.starttls()

    server.login(

        SMTP_EMAIL,

        SMTP_PASSWORD

    )

    return server


# =========================================================
# HTML EMAIL WRAPPER
# =========================================================

def build_email_template(

    title: str,

    heading: str,

    username: str,

    message: str,

    button_text: str,

    button_link: str,

    footer_note: str

) -> str:
    """
    Returns a reusable HTML email template.
    """

    return f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<style>

body{{
    margin:0;
    padding:40px;
    background:#f5f7fb;
    font-family:Arial,sans-serif;
}}

.container{{
    max-width:650px;
    margin:auto;
    background:#ffffff;
    border-radius:16px;
    overflow:hidden;
    box-shadow:0 10px 35px rgba(0,0,0,.08);
}}

.header{{
    background:#2563EB;
    color:#ffffff;
    padding:35px;
    text-align:center;
}}

.content{{
    padding:40px;
    color:#334155;
    line-height:1.8;
}}

.button{{
    display:inline-block;
    margin:30px 0;
    padding:15px 34px;
    background:#2563EB;
    color:#ffffff !important;
    text-decoration:none;
    border-radius:8px;
    font-weight:bold;
}}

.link{{
    margin-top:20px;
    word-break:break-all;
    color:#2563EB;
}}

.footer{{
    background:#F8FAFC;
    padding:25px;
    text-align:center;
    color:#64748B;
    font-size:13px;
}}

</style>

</head>

<body>

<div class="container">

<div class="header">

<h2>{title}</h2>

</div>

<div class="content">

<p>Hello <strong>{username}</strong>,</p>

<p>{message}</p>

<p style="text-align:center;">

<a href="{button_link}" class="button">

{button_text}

</a>

</p>

<p>

If the button above doesn't work,
copy and paste this link into your browser.

</p>

<p class="link">

{button_link}

</p>

<p>

{footer_note}

</p>

</div>

<div class="footer">

<strong>AI Website Audit Tool</strong>

<br>

AI-Powered Website Analysis Platform

</div>

</div>

</body>

</html>
"""

print("Connecting to Gmail...")

# =========================================================
# COMMON EMAIL SENDER
# =========================================================

def send_email(

    recipient: str,

    subject: str,

    html_body: str,

    text_body: str

) -> bool:
    """
    Sends an email using Gmail SMTP.
    """

    try:

        message = MIMEMultipart("alternative")

        message["From"] = f"{EMAIL_FROM} <{SMTP_EMAIL}>"

        message["To"] = recipient

        message["Subject"] = subject

        message.attach(

            MIMEText(

                text_body,

                "plain"

            )

        )

        message.attach(

            MIMEText(

                html_body,

                "html"

            )

        )

        server = create_smtp_connection()

        server.sendmail(

            SMTP_EMAIL,

            recipient,

            message.as_string()

        )
        
        print("Sending email...")
        print("Email sent successfully!")

        server.quit()

        return True

    except Exception as ex:

        print(f"Email Error: {ex}")

        return False
    
    # =========================================================
# PASSWORD RESET EMAIL
# =========================================================

def send_password_reset_email(
    user_email: str,
    user_name: str,
    reset_link: str
) -> bool:
    """
    Sends the password reset email.
    """

    subject = "Reset Your Password | AI Website Audit Tool"

    html_body = build_email_template(

        title="Reset Password",

        heading="Password Reset",

        username=user_name,

        message=(
            "We received a request to reset your password for your "
            "AI Website Audit Tool account. "
            "Click the button below to create a new password."
        ),

        button_text="Reset Password",

        button_link=reset_link,

        footer_note=(
            "This password reset link will expire in 30 minutes. "
            "If you did not request a password reset, you can safely "
            "ignore this email."
        )

    )

    text_body = f"""
        Hello {user_name},

        We received a request to reset your password.

        Open the following link:

        {reset_link}

        This password reset link expires in 30 minutes.

        If you did not request this password reset,
        please ignore this email.

        ----------------------------------------------------
        AI Website Audit Tool
        ----------------------------------------------------
        """

    return send_email(

        recipient=user_email,

        subject=subject,

        html_body=html_body,

        text_body=text_body

    )
    
    # =========================================================
# EMAIL VERIFICATION
# =========================================================

def send_verification_email(
    user_email: str,
    user_name: str,
    verification_link: str
) -> bool:
    """
    Sends account verification email.
    """

    subject = "Verify Your Email | AI Website Audit Tool"

    html_body = build_email_template(

        title="Verify Your Email",

        heading="Email Verification",

        username=user_name,

        message=(
            "Thank you for creating your AI Website Audit Tool account. "
            "Please verify your email address by clicking the button below."
        ),

        button_text="Verify Email",

        button_link=verification_link,

        footer_note=(
            "If you did not create this account, "
            "you can safely ignore this email."
        )

    )

    text_body = f"""
Hello {user_name},

Welcome to AI Website Audit Tool.

Please verify your email.

{verification_link}

If you did not create this account,
please ignore this email.

----------------------------------------------------
AI Website Audit Tool
----------------------------------------------------
"""

    return send_email(

        recipient=user_email,

        subject=subject,

        html_body=html_body,

        text_body=text_body

    )

# =========================================================
# LOGGING
# =========================================================

def log_email_success(
    email_type: str,
    recipient: str
):

    print(

        f"[EMAIL SUCCESS] "

        f"{email_type} "

        f"sent to "

        f"{recipient}"

    )


def log_email_error(
    email_type: str,
    recipient: str,
    error: Exception
):

    print(

        f"[EMAIL ERROR] "

        f"{email_type} "

        f"failed for "

        f"{recipient}"

    )

    print(error)