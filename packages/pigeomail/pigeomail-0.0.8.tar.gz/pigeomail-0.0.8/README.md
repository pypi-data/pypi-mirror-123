# pigeomail
A highly efficient and modular mail delivery framework for Python

##Install
```shell
pip install pigeomail
```
## How to use
```python
from pigeomail import Message,Mailer


if __name__ == "__main__":
    msg = Message()
    msg.From = "pigeomail"
    msg.To = ["xxx@gmail.com"]
    msg.Cc = []
    msg.Subject = "Hello, pigeomail is a highly efficient and modular mail delivery framework for Python."
    msg.Html = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        </head>
        <body>
            <h1>Hello world~</h1>
            <p>pigeomail is a highly efficient and modular mail delivery framework for Python.</p>
        </body>
        </html>
    """
    msg.attachments = [
        "test1.jpg",
        "test2.jpg",
    ]

    mailer = Mailer(
        host="xxxx.163.com",
        port=80,
        user="username@163.com",
        pwd="passwd",
    )
    mailer.send(msg)  # just send your message through the mailer
```
