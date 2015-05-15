#!/usr/bin/python

#script per selezionare casualmente gli esami per ogni "centro" del test
#e eseguire il test
import sys
import commands
import os 
import random
import time

if len(sys.argv)<4:
	print 'arg 1 dimesione del centro (grande, medio, piccolo)'
	print 'arg 2 numero di esami per il centro'
	print 'arg 3 percorso e nome file lista generale degli esami'
	print 'arg 4 percorso e file della chiave web-server'
	sys.exit()

dim_centro=sys.argv[1]
num_esami=sys.argv[2]
file_lista_gen=sys.argv[3]
path_chiave_server=sys.argv[4]

nome_file_lista_cent='lista_centro_'+dim_centro
file_lista_cent=open(nome_file_lista_cent,'w')
lista_casi=open(file_lista_gen,'r')
diz_casi={}
i=0
print str(nome_file_lista_cent)

#definizione tempo di attesa tra due esami in base alla dimensione del centro
if dim_centro=="grande":
	time_sleep=600
if dim_centro=="medio":
        time_sleep=1200
else:
	time_sleep=1800


for line in lista_casi:
	line=line.replace('\n','')
	diz_casi[i]=str(line)
	i=i+1
j=0
elenco_chiavi=range(0,i)
while (j < int(num_esami)):
	j=j+1
	caso_random=random.choice(elenco_chiavi)
	file_lista_cent.write(diz_casi[caso_random]+'\n')
lista_casi.close()
file_lista_cent.close()
#fine creazione lista random di casi

#copia dei casi estratti sulla macchina locale
#copio dal web server cosi' ho solo esami gia' zippati
lista_cent=open(nome_file_lista_cent,'r')
for riga in lista_cent:
	riga=riga.replace('\n','')
#	os.system("scp -r -i /Users/marcosaletta/id_rsa m5l@cloud-gw-211.to.infn.it:/home/m5l/magic5/data/"+riga+" /Users/marcosaletta/Documents/stress-test-CAD/casi/") da nodo cloud 
	os.system("scp -r -i "+path_chiave_server+" root@mag03xl.to.infn.it:/data/web-cases/"+riga+" /Users/marcosaletta/Documents/stress-test-CAD/casi/")
#rimuovo ROIs e logs
	os.system("rm -r /Users/marcosaletta/Documents/stress-test-CAD/casi/"+riga+"/ROIs")
	os.system("rm -r /Users/marcosaletta/Documents/stress-test-CAD/casi/"+riga+"/logs")
#rinomino il file e lo zip con + _stress
	os.system("mv /Users/marcosaletta/Documents/stress-test-CAD/casi/"+riga+" /Users/marcosaletta/Documents/stress-test-CAD/casi/"+riga+"_stress")
	os.system("mv /Users/marcosaletta/Documents/stress-test-CAD/casi/"+riga+"_stress/M5LC_"+riga+".zip /Users/marcosaletta/Documents/stress-test-CAD/casi/"+riga+"_stress/M5LC_"+riga+"_stress.zip")
lista_cent.close()
#fine copia casi estratti su macchina locale

#inizio copia dei casi estratti macchina locale -> web server 
#e lancio runM5L_on_cloud
lista_cent=open(nome_file_lista_cent,'r')
counter=0
for riga in lista_cent:
	counter=counter+1
        riga=riga.replace('\n','')
        os.system("(time scp -r -i "+path_chiave_server+" /Users/marcosaletta/Documents/stress-test-CAD/casi/"+riga+"_stress root@mag03xl.to.infn.it:/var/www/html/m5l/sites/all/modules/custom/casi_test/) 2> time_copy_"+riga)
#fine copia casi estratti macchina locale -> web server
#e lancio runM5L_on_cloud
	os.system("(time ssh -i "+path_chiave_server+" root@mag03xl.to.infn.it '/var/www/html/m5l/sites/all/modules/custom/m5l/runM5L_on_new_cloud.sh "+riga+"_stress /var/www/html/m5l/sites/all/modules/custom/casi_test') 2>time_exec_"+riga)
#aspetto prima di passare al successivo
	if counter<=int(num_esami)-1:
		time.sleep(int(time_sleep))
lista_cent.close()




