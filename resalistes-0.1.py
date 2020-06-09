#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import time
from operator import itemgetter, attrgetter
import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak
from reportlab.graphics.barcode import code128
from reportlab.graphics.barcode import eanbc, qr, usps
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

fichier =  'a.csv'

aujourdhui=datetime.date.today()
now=str(aujourdhui)
won=now[8:10]+"/"+now[5:7]+"/"+now[0:4]
#print("aujourd'hui : "+won)
if os.path.isdir(now)==0 :
    os.mkdir(now)
#duplique le fichier CSV dans T
#os.system('copy '+fichier+' T:\deconfinement\drive\listes\\'+now+"\\"+fichier)
#os.system('copy '+fichier+' C:\deconfinement\drive\listes\\'+now+"\\"+fichier)

# nb de jours avant expiration + retour
expiration=5
expirationtransit=8
retour=21
retourtransit=24
delai=datetime.timedelta(days=expiration)
dateexpiration=str(aujourdhui+delai)
dateexp=dateexpiration[8:10]+"/"+dateexpiration[5:7]+"/"+dateexpiration[0:4]

delai=datetime.timedelta(days=expirationtransit)
dateexpirationtransit=str(aujourdhui+delai)
dateexptransit=dateexpirationtransit[8:10]+"/"+dateexpirationtransit[5:7]+"/"+dateexpirationtransit[0:4]

delai=datetime.timedelta(days=retour)
dateretour=str(aujourdhui+delai)
dateretourlect=dateretour[8:10]+"/"+dateretour[5:7]+"/"+dateretour[0:4]

delai=datetime.timedelta(days=retourtransit)
dateretourtransit=str(aujourdhui+delai)
dateretourlecttransit=dateretourtransit[8:10]+"/"+dateretourtransit[5:7]+"/"+dateretourtransit[0:4]
#print("date expiration : "+dateexp)

entete=""
succ={"Bibliothèque Carnegie":"carnegie",
    "Bibliothèque du Chemin-Vert":"cheminvert",
    "Médiathèque Croix-Rouge":"croixrouge",
    "Bibliothèque Holden":"holden",
    "Médiathèque Jean Falala":"falala",
    "Médiathèque Laon-Zola":"laonzola",
    "Bibliothèque Saint-Remi":"saintremi",
    "Bibliobus urbain":"bibliobus",
    "Centre de documentation de l'ESAD":"esad",
    "Conservatoire (CRR)":"conservatoire"}

	 
# lecture du fichier
nbchamp=16
tableau=[]


# les chaines de caratères sont à nettyer, notamment les compléments de titres 
def nettoyage(txt):
    #Nettoie le corps de la chaine de caracteres
    txt=txt.replace(". -"," ")    
    txt=txt.replace("\\\'","\'")
    txt=txt.replace("\\\"","\"")
    txt=txt.replace("\""," ")
    txt=txt.replace(" ,",",")
    txt=txt.replace("/"," ")
    txt=txt.replace(": :",":")
    txt=txt.replace(", :",",")
    txt=txt.replace(", .",",")
    txt=txt.replace("', '",",")
    txt=txt.replace(".,",",")
    txt=txt.replace(",.",",")
    txt=txt.replace("    "," ")
    txt=txt.replace("   "," ")
    txt=txt.replace("  "," ")

    i=1 #répète cette opération tant qu'il y a encore du nettyage à effectuer sur la chaine de caractère
    while i==1:
        i=0
        #nettoie spécifiquement les premiers caratères de la chaine de caracteres
        if len(txt)>0:
            if txt[0]==",":
                txt=txt[1:]
                i=1
        if len(txt)>0:
            if txt[0]=="'":
                txt=txt[1:]
                i=1
        if len(txt)>0:
            if txt[0]==":":
                txt=txt[1:]
                i=1                
        if len(txt)>0:
            if txt[0]==" ":
                txt=txt[1:]
                i=1
        if len(txt)>0:
            if txt[0]=="-":
                txt=txt[1:]
                i=1
        #nettoie spécifiquement les derniers caratères de la chaine de caracteres        
        if len(txt)>0:
            if txt[-1]==",":
                txt=txt[0:-1]
                i=1
        if len(txt)>0:
            if txt[-1]==":":
                txt=txt[0:-1]
                i=1
        if len(txt)>0:
            if txt[-1]==" ":
                txt=txt[0:-1]
                i=1
        if len(txt)>0:
            if txt[-1]=="-":
                txt=txt[0:-1]
                i=1

    return txt

#with open(fichier,encoding='ISO-8859-1', newline='') as csvfile:

"""
Exemple sur https://docs.python.org/3/library/csv.html

>>> import csv
>>> with open('eggs.csv', newline='') as csvfile:
...     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
...     for row in spamreader:
...         print(', '.join(row))
Spam, Spam, Spam, Spam, Spam, Baked Beans
Spam, Lovely Spam, Wonderful Spam

"""
 


# UTF-8
#with open(fichier,encoding='UTF-8', newline='') as csvfile:
with open(fichier,encoding='ISO-8859-1', newline='') as csvfile:
    #reader = csv.reader(csvfile)
    spamreader = csv.reader(csvfile, delimiter=';', quotechar=' ')
    for row in spamreader:
        
        cell=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

        for i in range(16):
            cell[i]=str(row[i])

            
        
        """
        numchamp=0
        for car in texte:
            #print (car)
            if car==";":
                if numchamp==0:
                    txt=txt[2:]
                cell[numchamp]=txt
                #print("champ = "+txt)
                numchamp+=1
                txt=""

            else:
                txt+=car
        #print("txt = "+txt)
        if len(txt)<3:
            txt="vide13"
        
        cell[numchamp]=txt[0:-2]

        """
        
        tableau.append(cell)
        
#print (tableau[10])
del tableau[0]
# tableau trié par succursale du document
tabdoc=list(sorted(tableau, key=itemgetter(0)))
#création du répertoire de destination


def envoipdf(cell): 
    donnee=""
    tab=list(sorted(cell, key=itemgetter(10,1,2)))
    succursale=tab[0][0]
    dest=succ[succursale]
    print(succursale+"=>"+dest)
    destination = canvas.Canvas(now+"/"+dest+"-"+now+".pdf") 
    lect=""
    nbligne=len(tab)
    print (nbligne)
    premierepage=1
    hautdepage=810
    y=hautdepage
    x=20
    xmid=300
    deltay=15

    for ligne in tab:
        transit=0

        if lect!=ligne[10]:

            if premierepage==1:
                premierepage=0
            else:
                #https://stackoverflow.com/questions/3593193/add-page-break-to-reportlab-canvas-object
                destination.pageNumer=2
                destination.showPage()
                #PageBreak.drawOn(destination, 0, 1000, 0)                
                y=hautdepage
                
            lect=ligne[10]
            lecteur=lect
            
            if lecteur[0:3]=="M. ":
                lecteur=lecteur[3:]
            elif lecteur[0:4]=="Mme ":
                lecteur=lecteur[4:]
            if len(lecteur)>33:
                lecteur=lecteur[0:29]+"..."
            destination.setFont("Helvetica", 10)            
            destination.drawString(x,y,dest)
            y -= int(1.5*deltay)
            destination.setFont("Helvetica", 18)
            destination.drawString(x,y,lecteur)
            y-=deltay
            destination.setFont("Helvetica", 10) 
 ###OH   
            #cb lecteur en code barre128
            y+=10            
            txt=ligne[11][1:-1]
            barcode128Std = code128.Code128(txt, barWidth=0.3*mm, barHeight=8*mm, checksum=0)
            barcode128Std.drawOn(destination,x+400,y)
            y-=10
            """y -= int(0.7*deltay)
            destination.setFont("Helvetica", 10)
            destination.drawString(x+400,y,txt)"""
            
### OH
				
        # si la commande fait plus d'une page    
        if (y-5*deltay)<10 :
            destination.setFont("Helvetica", 12)            
            destination.drawString(350,5,"Suite page suivante.../...")
            
            destination.pageNumer=2
            destination.showPage()
            y=hautdepage
            lect=ligne[10]
            destination.setFont("Helvetica", 10)            
            destination.drawString(x,y,dest)

            destination.setFont("Helvetica", 12)            
            destination.drawString(450,y,"... suite")
            
            y -= int(1.5*deltay)
            destination.setFont("Helvetica", 18)
            destination.drawString(x,y,lecteur)
            y-=deltay
            destination.setFont("Helvetica", 10)
            #cb lecteur en code barre128
            y+=10            
            txt=ligne[11][1:-1]
            barcode128Std = code128.Code128(txt, barWidth=0.3*mm, barHeight=8*mm, checksum=0)
            barcode128Std.drawOn(destination,x+400,y)
            y-=10
            
        #titre
        y-=deltay        
        txt=ligne[4]
        destination.setFont("Helvetica", 15)
        destination.drawString(x,y,txt)

            
        txt=str(ligne[13])+" - "+str(ligne[15])#+" - "+str(ligne[15])
        txt=nettoyage(txt)

        
        if txt!="":
            y-=deltay    
            destination.setFont("Helvetica", 10)
            destination.drawString(x,y,txt)

        #envoyer à
        if ligne[7]!=succursale:
            txt="=> "+ligne[7]
            destination.setFont("Helvetica", 15)
            destination.drawString(xmid+80,y,txt)
            transit=1

            
# ------------Ligne suivante -----------------
        y-=deltay

        
        
        #cote - type doc - secteur
        txt=ligne[2]+" - "+ligne[5]+" - "+ligne[1]
        destination.setFont("Helvetica", 12)
        destination.drawString(xmid,y,txt)

        # date prise en charge        
        txt="Traité le : "+won
        destination.setFont("Helvetica", 12)
        destination.drawString(x,y,txt)


            
# ------------Ligne suivante -----------------
        y-=deltay
        

        # date réservation - rappel succ
        txt=ligne[3]+" - "+ligne[10]
        destination.setFont("Helvetica", 7)
        destination.drawString(xmid,y,txt)

        # date d'expiration
        if transit==1:
            date=dateexptransit
        else:
            date=dateexp
        txt="Expire le : "+date
        destination.setFont("Helvetica", 12)
        destination.drawString(x,y,txt)

        
            
# ------------Ligne suivante -----------------
        y-=int(1.5*deltay)
        

        #cb exemplaire en code barre128 + CB

        
        txt=ligne[6][1:-1]
        barcode128Std = code128.Code128(txt, barWidth=0.3*mm, barHeight=5*mm, checksum=0)
        barcode128Std.drawOn(destination,xmid-15,y)

        txt=ligne[6][1:-1]
        txt=txt[0:-4]+" 5100"
        destination.setFont("Helvetica", 10)
        destination.drawString(xmid+120,y,txt)

        if "Réservé" in ligne[8] :
            txt=" Retour-reservé"
            destination.setFont("Helvetica", 13)
            destination.drawString(xmid+200,y,txt)

	# date de retour
        if transit==1:
            date=dateretourlecttransit
        else:
            date=dateretourlect
        txt="A rendre avant le : "+date
        destination.setFont("Helvetica", 14)
        destination.drawString(x,y,txt)
		           
    


        

        y -= int(1.5*deltay)

        
        
        #if ligne[7]!=succursale:
            #donnee+="Envoyer à  => <b>"+ligne[7]+"</b><br>\n"
                   
    destination.save()

# -------------- fin d'envoi de fichier ------------
nbligne=len(tabdoc)
print(nbligne)

sucdoc=tabdoc[0][0]
cell=[]
for line in tabdoc:
    if line[0]==sucdoc:
        cell.append(line)
    else :
        envoipdf(cell)
        cell=[]
        cell.append(line)
        sucdoc=line[0]
envoipdf(cell)  	 

##OH : ouvrir le pdf de Falala du jour dans Adobe Reader 
def imprfal():
    contenu=open("impr_fal.bat", "w")
    comm="\"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe\" /P "
    chemin="T:\deconfinement\drive\listes\\"+now+"\\falala"+"-"+now+".pdf"
    comm+=chemin 
    print(comm)
    contenu.write(comm)
    contenu.close()
    os.system('impr_fal.bat')
	

reponse=input('Voulez-vous imprimer pour Falala ?(y/n)')

if reponse=="y":
    imprfal()
else:
    print('ok')
