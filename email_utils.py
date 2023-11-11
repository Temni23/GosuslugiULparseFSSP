import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import APP_EMAIL, APP_EMAIL_PASSWORD


def send_vip_to_user(file:bytes, recipient_email:str) -> None:
    """Функция используется для отправки емэйла с файлом пользователю."""
    email = APP_EMAIL
    password = APP_EMAIL_PASSWORD
    target_email = recipient_email

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = target_email
    msg['Subject'] = f'Поступило новое постановление от ФССП'
    text_for_email = 'Выявлено новое постановление от ФССП'
    msg.attach(MIMEText(text_for_email, 'html'))

    # Добавление вложения в письмо
    file_to_email = file
    attachment = MIMEApplication(file_to_email, Name="attachment")
    attachment['Content-Disposition'] = 'attachment; filename="attachment.pdf"'
    msg.attach(attachment)

    try:
        mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(email, password)

        mailserver.sendmail(email, target_email, msg.as_string())

        mailserver.quit()
    except smtplib.SMTPException as e:
        print(f'Ошибка: Невозможно отправить сообщение - {str(e)}')
