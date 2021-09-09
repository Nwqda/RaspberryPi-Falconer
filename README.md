
# Raspberry Pi Falconer
Raspberry Pi Falconer is a useful tool that can be used to find Raspberry Pi with open SSH port worldwide.
To find this, the tool use Shodan search engine with its API, and with the help of the Shodan dorks, target only Raspberry Pi devices. Once a target detected, RaspberryPi Falconer will attempt to initialize a connection with it.

![RaspberryPi Falconer logo](https://i.ibb.co/jRGGZkf/Raspberry-Pi-Falconer-logo.png)

RaspberryPi Falconer is not a perfect tool at the moment but provides basic functionalities to automate the search of Raspberry devices with SSH port open on Shodan and try to connect to it with the default SSH combo credential, `pi` and `raspberry`. 
There is also the possibility to save the result of a query in `.CSV` or `.TXT` (at moment) once the research completed.

### Requirement
* Python 3 (Tested with Python 3.8.5)
* Shodan Account (API key)

### Installation
Clone this repository and run:
```shell
pip install -r requirements.txt
```
#### Usage
```
python3 rpi-falconer.py
```
Then let yourself be guided!

![RaspberryPi Falconer Cli](https://i.ibb.co/MsH3Y03/rpi-falconer.png)

### Contribution
Please consider contributing dorks that can reveal Raspberry Pi devices on Shodan.

### List of Dorks
I am not categorizing at the moment. Instead, I am going to just the list of dorks with a description. Many of the dorks can be modified to make the search more specific or generic.

 Dork                                           | Description
------------------------------------------------|--------------------------------------------------------------------------
"dnsmasq-pi-hole" "Recursion: enabled" | Pi-hole Open DNS Servers.

### Note
FOR EDUCATIONAL PURPOSE ONLY.
