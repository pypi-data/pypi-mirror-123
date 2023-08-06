# Simple Mail Sender

This email sender python package gives ease of acess to Python's built-in SMTP module. It supports plaintext and HTML based messages and only supports Python3 version.

## Features

- Reduces the configurations needed for built-in modules.
- Can send emails fetching from plain text or through HTML templates.
- TLS or SSL can be used to connect to the SMTP servers.

## Installation

```bash
pip install emailservice
```

## Usage

## Sending a simple plaintext message

```python
    plaintext = 'This is our text message'
```

- Create a EmailService object. The EmailService object allows you to connect to an SMTP server by specifying the server address and port, as well as your username and password.

```python
    testEmailService = EmailService('username@server.com', 'password', ('smtp.server.com', 465), use_SSL=True)
```

- Now we set the plaintext message to the email's body.

```python
    testEmailService.set_message(plaintext, "Subject", 'John Doe <j.doe@server.com>')
```

- Set the recipients for your email by specifying a complete list/tuple of all the mentioned recipients.

```python
    testEmailService.set_recipients(['recepient1@server.com', 'recepient2@server.com'])
```

- Here we connect to the SMTP server you specified when creating the EmailService object.

```python
    testEmailService.connect()
```

- Below method sends the same message to all listed recipients. By default the connection to the SMTP server is closed once the email has been sent to all currently listed recipients. If you want to send further emails without having to reconnect to the SMTP server, you can make the close_connection as False as shown below.

```python
    testEmailService.send_all(close_connection=False)
```

## Sending an HTML message

- Import or write both a plaintext message and HTML message, stored in separate variables. This plaintext is only shown in cases where email clients do not support HTML markup.

```python
    plaintext = 'This is our message'
    html = '<b>This</b> is our message'
```

- Set the HTML and plaintext messages as the email's body.

```python
    testEmailService.set_message(plaintext, "Subject line", 'John Doe', html)
```

## Recommended SMTP server settings

Outlook:

- Using TLS: smtp.live.com, port 587

Gmail:

- Using SSL: smtp.gmail.com, port 465
- Using TLS: smtp.gmail.com, port 587

* These connections may be blocked if 'Access for less secure apps' is disabled in your Google Account settings
