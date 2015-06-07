import smtplib
import mimetypes

from email.mime.text import MIMEText
from email.encoders import encode_base64


class Correo:
    # Variables
    __user = ""
    __passwd = ""
    __remitente = ""

    #Constructor
    def __init__(self, user, passwd, remitente):
        self.__user = user
        self.__passwd = passwd
        self.__remitente = remitente

    #Set's y Get's
    def setUser(self, user):
        self.__user = user

    def getUser(self):
        return self.__user

    def setPasswd(self, passwd):
        self.__passwd = passwd

    def getPasswd(self):
        return self.__passwd

    def setRemitente(self, remitente):
        self.__remitente = remitente

    def getRemitente(self):
        return self.__remitente

    def enviarMensaje(self, destinatario, nombreDestinatario):
        #Construccion del mensaje
        mensaje = "¡¡¡ Felicitaciones !!! \n Usuario " + nombreDestinatario + " sus datos han sido registrado exitosamente."
        texto = MIMEText(mensaje)
        texto['From'] = self.__remitente
        texto['To'] = destinatario
        texto['Subject'] = "CREATIC CIER-SUR COLOMBIA"

        #Conexion con el servidor
        email = smtplib.SMTP('smtp.gmail.com', 587)
        email.ehlo()
        email.starttls()
        email.ehlo()

        #Autenticacion de Usuario
        email.login(self.__user, self.__passwd)

        #Envio del mensaje
        email.sendmail("ciersurcolombia@gmail.com", destinatario, texto.as_string())

        #Cierre de la conexion SMTP con Gmail
        email.close()

        print("Mensaje enviado satisfactoriamente")