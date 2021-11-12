from ssl import get_protocol_name
import time
import pymongo
from pymongo import collection
#from Collection import count_documents
from bson.json_util import dumps
import json
import ast
#------------------------------------------- les bots utiliser 
from webhookScraping import webhookBotScrap     #envoie la notif du scraping dans le canal scraping_alert 
from webhookGetEmails import webhookBotGetemail #par analogie 
from webhookSend import webhookBotSend          #par analogie


timeSleep = 30 #lw9t libin kola parcours dyal checking



try:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    
    DbOfClient = client['kbot']
    
    colClient = DbOfClient['survillance']
except :
    print("Error loading database")

    

try : 
    cursor = colClient.find()   #cusor li kayparcouris la BD , pas = document 
except :
    print("Error loading cursor")

x = dumps(cursor)

json_acceptable_string = x.replace("'", "\"")


try:
    L = ast.literal_eval(x)


except:
    json_acceptable_string = x.replace("'", "\"")
    L = json.loads(json_acceptable_string)     #fiha la BD initiale 


#L = json.loads(json_acceptable_string)


n = cursor.count()   #kan3rfo hna ch7al mn document tl3 had lcursor 


cursor.close()


'''
 La logique utiliser (algorithme): 
           # télécharger la base de donnée initiale dans <<<L>>> 
           # comparer chaque periode de <timeSleep> la base de donnée avec le L 
           #la comparaison se fait via le curseur qui parcours la base 
                        # Si il trouve un changement il le signale et modifie L et pass 
'''


while (1):

    print("start sleep")

    time.sleep(timeSleep)

    print("end_sleep")

    i = 0

    stringMesseage = ""

    cursor = colClient.find()

    for document in cursor:

      #      del document['_id']

        #partie 1 : scarpping check ?

        if document['Scraping'] == False:  # rj3 False

            if L[i]['Scraping'] == True:  # Kan True

                #stringMesseage += "_Le Scrapping_ est commencé pour *%s* " %document['Name']

                print("Scraping stped for   ", document['Name'])  # send notiff

                L[i]['Scraping'] = False

                time.sleep(1)

                if (document['finished_scraping'] == 'bug'):

                    stringMesseage = ""

                    stringMesseage += " * Le *Scraping* pour *%s* s'est arreté \n *    Cause : bug :bug:" % document[
                        'Name']

                    stringMesseage += "\n * le _nombre_ _de_ _contacts_ _scrappé_ est  *%d* " % document[
                        'ScrappedContacts']

                    print("Scraping for %s stoped due to bug" %
                          document['Name'])

                    print("\nLe  nombre de contacts scrappé est : *%d* " %
                          document['ScrappedContacts'])

                    webhookBotScrap(
                        stringMesseage + "\n__________________________________")

                else:

                    stringMesseage = ""

                    stringMesseage += " * Le *scrapping* _est_ _terminé_ _avec_ _succes_ pour *%s*" % document[
                        'Name'] + "\n" + "* le _nombre_ _de_ _contacts_ _scrappé_ est  : *%d* " % document['ScrappedContacts']

                    stringMesseage += '\n * *à* :timer_clock: _%s_' % document['finished_scraping']

                    print("Scraped succefully")

                    print("number of scraped %d" %
                          document['ScrappedContacts'])

                    print("-|-|-")

                    webhookBotScrap(stringMesseage +
                                    "\n__________________________________")

        else:  # rj3 true

            if L[i]['Scraping'] == False:  # kant false

                stringMesseage += '* Le *Scrapping* _est_ _commencée_ pour *%s* \n' % document['Name']

                stringMesseage += '* *à* :timer_clock: _%s_' % document['StartingScraping_date']

                print('Scraping started for  ',
                      document['Name'])  # send notifff

                L[i]['Scraping'] = True

                webhookBotScrap(stringMesseage +
                                "\n__________________________________")

        '''--------------------------------------------------------------------'''

        #partie 2 : Send connection check check ?

        if document['invitationProcess'] == False:  # rj3 False

            stringMesseage = ""

            if L[i]['invitationProcess'] == True:  # Kan True

                print("send connection stped for   ",
                      document['Name'])  # send notiff

                L[i]['invitationProcess'] = False

                time.sleep(1)

                if (document['finished_invitationProcess'] == 'bug'):

                    stringMesseage = "* Le processus *send* *connection* s'est arreté pour   *%s*  " % document['Name']

                    stringMesseage += " \n" + \
                        "* _Cause_ : Bug  :bug" % document['Name']

                   

                    stringMesseage += '* *à* :timer_clock: _%s_' % document['StartingScraping_date']

                    print("send connection for %s stoped due to bug" %
                          document['Name'])
                else:
                    stringMesseage = "* Le processus *send* *connection* s'est arreté pour   *%s*  " % document['Name']

                    stringMesseage += "\n * *Send* *connection* s'_est_ _terminé_ _avec_ _succes_ pour *%s*" % document[
                        'Name']

                    stringMesseage += '\n* *à* :timer_clock: _%s_' % document['finished_invitationProcess']

                webhookBotSend(stringMesseage +
                               "\n__________________________________")

        else:  # rj3 true
            if L[i]['invitationProcess'] == False:  # kant false

                print('send connection started for  ',
                      document['Name'])  # send notifff

                stringMesseage = "* *Send* *connection* est lancé pour *%s*" % document['Name']

                L[i]['invitationProcess'] = True

                webhookBotSend(stringMesseage +
                               "\n__________________________________")

        '''---------------------------------------------------------------------''' 

        #partie 2 : getemails check check ?

        if document['getEmails'] == False:  # rj3 False

            stringMesseage = ""

            if L[i]['getEmails'] == True:  # Kan True

                print("getEmails stped for   ",
                      document['Name'])  # send notiff

                L[i]['getEmails'] = False

                time.sleep(1)

                if (document['finished_getEmails'] == 'bug'):

                    stringMesseage = "* Le processus *get* *Emails* :email: s'est arreté pour" + \
                        "*" + document['Name']+"*"

                    stringMesseage += "* Cause : bug :bug:" 

                    stringMesseage += "\n" + \
                        "* _Nombre_ d'email getter est  *%d*" % document['getEmailsContacts']

                    print("get emails for %s stoped due to bug" %
                          document['Name'])

                    print("nombre d'email scrped %d" %
                          document['getEmailsContacts'])

                    webhookBotGetemail(
                        stringMesseage + "\n__________________________________")

                else:

                    stringMesseage = "* Le processus *get* *Emails* :email: s'est terminé corectement pour" + \
                        "*" + document['Name']+"*"

                    stringMesseage += "\n * Nombre *d'email*   *%d*" % document['getEmailsContacts']

                    print("get emails for %s ended succ" % document['Name'])

                    print("nombre d'email scrped %d" %
                          document['getEmailsContacts'])

                    webhookBotGetemail(
                        stringMesseage + "\n__________________________________")

        else:  # rj3 true

            if L[i]['getEmails'] == False:  # kant false

                stringMesseage += '\n * Le procesuss *getEmail* est commencé pour   ' + \
                    "*"+document['Name']+"*" + "\n * à :timer_clock: " + "*"+document['StartingGetEmails_date'] + "*"

                print('getEmails started for  ',
                      document['Name'])  # send notifff

                L[i]['getEmails'] = True

                webhookBotGetemail(
                    stringMesseage + "\n__________________________________")

        i += 1
