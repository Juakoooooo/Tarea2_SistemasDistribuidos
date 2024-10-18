import smtplib
from email.mime.text import MIMEText

def enviar_correo(destinatario, mensaje):
    remitente = "doe933331@gmail.com"  # Reemplaza con tu correo
    contraseña = "osqc ytkv ewpv yhiv"  # Reemplaza con tu contraseña de aplicación

    msg = MIMEText(f"Enviando mensaje desde la fake account: {mensaje}")
    msg['Subject'] = 'El pepe'
    msg['From'] = remitente
    msg['To'] = destinatario

    # Conectar al servidor SMTP de Gmail
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remitente, contraseña)
            server.sendmail(remitente, destinatario, msg.as_string())
            print("Correo de prueba enviado con éxito")
    except Exception as e:
        print(f"Error enviando correo: {e}")

# Prueba de envío de correo
enviar_correo("thania.godoy@mail.udp.cl", "El pepe.")
