import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import APP_EMAIL, APP_EMAIL_PASSWORD, TRIGGER_TO_EMAIL


def send_vip_to_user(file: bytes, recipient_email: str) -> None:
    """Функция используется для отправки письма с файлом пользователю."""
    email = APP_EMAIL
    password = APP_EMAIL_PASSWORD
    target_email = recipient_email

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = target_email
    msg['Subject'] = f'Поступило новое постановление от ФССП'
    text_for_email = (f'Выявлено новое постановление о возбуждении '
                      f'исполнительного производства в отношении '
                      f'{TRIGGER_TO_EMAIL.upper()}, постановление во вложении')
    msg.attach(MIMEText(text_for_email, 'html'))

    # Добавление вложения в письмо
    file_to_email = file
    attachment = MIMEApplication(file_to_email, Name="attachment")
    attachment['Content-Disposition'] = 'attachment; filename="attachment.pdf"'
    msg.attach(attachment)

    try:
        sending_email(email, password, target_email, msg)
        print(f'Письмо успешно отправлено')
    except smtplib.SMTPException as e:
        print(f'Ошибка: Невозможно отправить сообщение - {str(e)}')


def send_email_to_user(recipient_email: str, text_for_email: str) -> None:
    """Функция используется для отправки письма без файла пользователю."""
    email = APP_EMAIL
    password = APP_EMAIL_PASSWORD
    target_email = recipient_email

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = target_email
    msg['Subject'] = (f'При проверке Госулсуг найдено ИП в отношении'
                      f' {TRIGGER_TO_EMAIL.upper()}')
    text_for_email = text_for_email
    msg.attach(MIMEText(text_for_email, 'html'))

    try:
        sending_email(email, password, target_email, msg)
        print(f'Письмо успешно отправлено')
    except smtplib.SMTPException as e:
        print(f'Ошибка: Невозможно отправить сообщение - {str(e)}')


def sending_email(email, password, target_email, msg):
    mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(email, password)

    mailserver.sendmail(email, target_email, msg.as_string())

    mailserver.quit()


def get_text_for_email(dbtr_name, supplier_org_name, number_doc,
                       id_organ_name, id_date, delo_num) -> str:
    text = (f'При проверке личного кабинета Госуслуг обнаружено '
            f'исполнительное производств в отношении {dbtr_name}.\n'
            f'Возбуждено в {supplier_org_name}\n'
            f'На основании исполнительного документа {number_doc}\n'
            f'Вынесенного органом {id_organ_name} {id_date}\n'
            f'Номер исполнительного производства {delo_num}\n'
            f'Сообщите об этом письме юристу!')
    return text
