import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    # Configuración del remitente y la contraseña
    from_email = 'strayscloud@gmail.com'
    password = 'wprj pxmo qyae eslz'  # Usar contraseña de aplicación si es 2FA está activado en Gmail

    # Creación del mensaje
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email) if isinstance(to_email, list) else to_email  # Asegúrate de que to_email sea una cadena
    msg['Subject'] = subject

    # Adjuntar el cuerpo del mensaje como texto plano
    msg.attach(MIMEText(body, 'plain'))

    # Conectar al servidor SMTP de Gmail y enviar el correo
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Usar 465 si es con SSL
    server.starttls()  # Iniciar TLS
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)  # Aquí to_email puede ser una lista
    server.quit()

