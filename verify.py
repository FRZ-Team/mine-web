import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = 'th3mcgrief@gmail.com'
EMAIL_PASSWORD = 'rcsauhzjravvoutf'


def verify(the_mail, name, number):
    msg = EmailMessage()
    msg['Subject'] = 'Подтверждение личности'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = the_mail
    msg.set_content(f"""зравствуйте {name}\nмы получили от вас запрос на изменение пароля,
Чтобы подтвердить запрос введите данный номер:\n{number}""")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
