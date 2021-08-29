from PIL import Image
import numpy as np
import sys

js_path = sys.argv[1]
option = sys.argv[2]
message = sys.argv[3]

def encrypt_text(message):
    #message = "je m'appelle test"
    message = "|-|-|"+message+"|-|-|"
    BinMessage = []
    for i in message: #transforme chaque lettre en octet
        BinMessage.append(format(ord(i), "08b")) #formatage
    BinMessage = ''.join(BinMessage)#transforme la liste des octets, en (une suite sans espaces)
    return BinMessage

def encrypt_into_image(message):

    BinMessage = encrypt_text(message)

    if len(BinMessage) <= ImgArray.size: 

        messageIndex = 0 #compteur 
        messageSize = len(BinMessage)
        
        for dim in range(3): #parcours tableau
            for columns in range(width): #parcours tableau
                for lines in range(height): #parcours tableau

                    value = ImgArray[lines, columns, dim] #récupère valeur du pixel
                    value = format(int(value), "08b") #transforme en binaire
                    value = (int(value[:-1] + BinMessage[messageIndex], 2)) #enlève dernier bit et remplace par celui de BinMessage
                    #print(value)
                    ImgArray[lines, columns, dim] = value

                    if messageIndex == messageSize - 1: #quand tout texte caché dans image:
                        
                        print(ImgArray[0:16, 0, 0])
                        print("finished")
                        pil_image=Image.fromarray(ImgArray) #transformer tableau en image

                        new_path = js_path.split(".")
                        new_path[0] += "_steg."
                        new_path = "".join(new_path)

                        pil_image.save(new_path) #save
                        return "ok" #pour stopper boucle

                    else: 
                        messageIndex += 1 #sinon ajoute un au compteur et recommence

        

    else:
        print("The text couldn't be hidden into the image because the image is too small to contain this text\n Please extend the image")

def decrypt():

    text = []

    #print(ImgArray[0:16, 0, 0])

    for dim in range(3): #parcours de la même façon qu'à l'encodage
        for columns in range(width):
            for lines in range(height):
                
                value = ImgArray[lines, columns, dim] #récupère valeur en chiffre
                value = format(int(value), "08b") #la met en bit
                last_bit = value[-1] #récupère dernier bit de l'octet 
                text.append(last_bit) #les met à la suite dans text

    text = "".join(text)


    Count = 0
    Message = []
    BinSize = len(text)
    Times = BinSize / 8 - 1

    for octet in range(int(Times)):

        octet = text[Count:Count+8]
        ascii = int(octet, 2)
        character = chr(ascii) #récupère caractère qui correspond au nombre
        Message.append(character)
        Count += 8

    Message = "".join(Message)
    Message = Message.split("|-|-|")[1]
    print(Message)
   


#path = input("What's the path of your image ?")



img = Image.open(js_path)
width, height = img.size

ImgArray = np.zeros((height, width, 3), dtype=np.uint8) #initialise tableau de la taille de l'image


for columns in range(width): #rempli tableau avec pixel image (1e plan pour r, 2e pour v, 3e pour b)
    for lines in range(height):
        r,v,b = img.getpixel((columns,lines)) #(x, y)
        ImgArray[lines, columns, 0] = r
        ImgArray[lines, columns, 1] = v
        ImgArray[lines, columns, 2] = b





if int(option) == 0:
    encrypt_into_image(message)


elif int(option) == 1:
    decrypt()





        
        





    """
    i = 0
    octet = []
    finally_text = []

    for num in range(len(text)): #pour trancher tout les 8 bits et faire des octets 
        if i != 8:
            bit = text[num]
            octet.append(bit)
            i += 1
        else:
            octet = "".join(octet) 
            #print(octet)
            ascii = int(octet, 2) #met octet en int
            character = chr(ascii) #récupère caractère qui correspond au nombre
            finally_text.append(character) #ajoute à liste de caractère 
            i = 0   # on remet le compteur de bit à 0
            octet = [] #on retransforme octet en liste
    
    #transforme liste en str
    finally_text = "".join(finally_text)
    #print(finally_text)
    """