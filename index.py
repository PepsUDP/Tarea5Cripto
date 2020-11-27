import imaplib, email
import re

user = 'jose.duran@mail.udp.cl'
f = open("pass.txt")
for line in f:
    password = line.split()[0]
f.close()
imap_url = 'imap.gmail.com'

def format(date):
    date = date.split('/')
    if date[1] == '01' or date[1] == '1':
        date[1] = 'Jan'
    elif date[1] == '02' or date[1] == '2':
        date[1] = 'Feb'
    elif date[1] == '03' or date[1] == '3':
        date[1] = 'Mar'
    elif date[1] == '04' or date[1] == '4':
        date[1] = 'Apr'
    elif date[1] == '05' or date[1] == '5':
        date[1] = 'May'
    elif date[1] == '06' or date[1] == '6':
        date[1] = 'Jun'
    elif date[1] == '07' or date[1] == '7':
        date[1] = 'Jul'
    elif date[1] == '08' or date[1] == '8':
        date[1] = 'Aug'
    elif date[1] == '09' or date[1] == '9':
        date[1] = 'Sep'
    elif date[1] == '10':
        date[1] = 'Oct'
    elif date[1] == '11':
        date[1] = 'Nov'
    elif date[1] == '12':
        date[1] = 'Dec'
    date[2] = '20'+date[2]
    date = date[0]+'-'+date[1]+'-'+date[2]
    return date

def searchMID(value, date, con):
    print("Recopilando Message-IDs emitidos por la dirección "+value+" desde la fecha "+date+".")
    result, data = con.search(None, 'FROM', '"{}"'.format(value), '(SINCE '+date+')')
    f = open("mid.txt", "a")
    f.write("----- BEGIN EMISOR: "+value+" -----\n")
    for num in data[0].split():
        result, data = con.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
        data = data[0][1].decode("utf-8").split('<')[1].split('>')[0]
        f.write("\n")
        f.write(data)
        print(data)
    f.write("\n")
    f.write("\n----- END EMISOR: "+value+" -----\n")
    f.close()

def validate(regex, value, date, con):
    validos = 0
    novalidos = 0
    print("Buscando emails emitidos por la dirección "+value+" desde la fecha "+date+".")
    result, data = con.search(None, 'FROM', '"{}"'.format(value), '(SINCE '+date+')')
    for num in data[0].split():
        result, data = con.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
        data = data[0][1].decode("utf-8").split('<')[1].split('>')[0]

        x = re.search(regex, data)
        print(data)
        
        if x:
            print("Message-ID cumple con la Regex ingresada!")
            validos = validos + 1
        else:
            print("Message-ID NO cumple con Regex ingresada.")
            novalidos = novalidos + 1
    
    print("Correos válidos:", validos, "\nCorreos no válidos:", novalidos)
    
    if novalidos > 0:
        print("¡Cuidado! El emisor puede haber sido suplantado durante el intervalo de tiempo ingresado.")
    
    return data

con = imaplib.IMAP4_SSL(imap_url)
try:
    con.login(user,password)
except Exception as err:
    print('ERROR:', err)

con.select("INBOX")

f = open("info.csv", "r")
cant = 0
for line in f:
    cant = cant + 1
f.close()

i = 0
regex = []
regex = [0 for i in range(cant)]
emisor = []
emisor = [0 for i in range(cant)]
fecha = []
fecha = [0 for i in range(cant)]

f = open("info.csv", "r")
for line in f:
    line = line.split(", ")
    regex[i] = line[0]
    emisor[i] = line[1]
    fecha[i] = line[2].strip()
    i = i + 1

f.close()

# searchMID(emisor[0], format(fecha[0]), con)

for i in range(cant):
    validate(regex[i], emisor[i], format(fecha[i]), con)

