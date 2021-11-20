error = False
try:
    import requests
except Exception:
    error = True
    print('Run: pip install requests')

try:
    from bs4 import BeautifulSoup
except Exception:
    error = True
    print('Run: pip install beautifulsoup4')

try:
    from colorama import Fore, init, Style
except Exception:
    error = True
    print('Run: pip install colorama')

if(error):
    exit()


init()

""" ips = ["X.Y.X.Y", "X.Y.X.Y"] """
ips = []

if(len(ips) == 0):
    print('No IPs to check')
    exit()

url = "https://blacklistalert.org/"

session = requests.Session()

response = session.get('https://blacklistalert.org/')


headers = {
    'Cookie': 'PHPSESSID='+session.cookies.get_dict()['PHPSESSID']
}

for x in ips:

    payload = {'q': x}

    response = requests.request("POST", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, 'html.parser')
    tabla = soup.select('table')[0]

    elementos = tabla.select('tr')
    elementosOkey = tabla.findAll('font', color='green')
    elementosFail = tabla.findAll('font', color='red')

    if(len(elementos) == len(elementosOkey)):
        print(Fore.GREEN + x.ljust(150) + "Okey")
    else:
        print(Fore.RED + x.ljust(150) + "" +
              str(len(elementosOkey)) + "/" + str(len(elementos)))
        print(Style.RESET_ALL)
        print("".ljust(20) + "Blocklists".ljust(70) + "Why is it blocked?")
        print("".ljust(20) +"".ljust(110, '-'))
        for index in elementosFail:
            elemento = index.parent.parent.parent
            websiteReport = elemento.select('td.left')[0].text
            websiteUrlReport = elemento.select('a')[0].attrs['href']
            print("".ljust(20) +websiteReport.ljust(70) + websiteUrlReport)

    print("")
