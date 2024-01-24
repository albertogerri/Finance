import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_table_url_selenium_driverless_xpath_nointestazione(url, xpaths,driver): #funzion con selenium ma più lento
    flag_failed=0
    # Utilizza il webdriver di Chrome con options per rendere il tutto più veloce
    driver.get(url)

    # Attendi che la pagina si carichi completamente (puoi regolare il valore in base alle esigenze)
    driver.implicitly_wait(10)

    # Trova tutte le tabelle nella pagina con xpath specificato
    tabelle=[]
    for i, xpath in enumerate(xpaths):
        try:
            # tab=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute("outerHTML")
            tab=driver.find_element(By.XPATH, xpath).get_attribute('innerHTML')
            tab=BeautifulSoup(tab,'lxml')
            tabelle.append(tab)
        except:
            print('Xpath ' + str(i)+' non trovato. flag_failed=1')
            flag_failed=1
            break

    # Inizializza un elenco di DataFrame pandas
    dataframes = []
    # Itera attraverso le tabelle
    for tabella in tabelle:
        # Estrai i dati dalla tabella e crea un DataFrame pandas
        dati_tabella = []
        intestazioni = []

        righe = tabella.find_all('tr')
        for i, riga in enumerate(righe):
            celle = riga.find_all(['th', 'td'])
            riga_dati = []
            for cella in celle:
                riga_dati.append(cella.get_text().strip())
            dati_tabella.append(riga_dati)

        # Crea un DataFrame pandas
        df = pd.DataFrame(dati_tabella)
        df=df.set_index(0)
        df=df.rename_axis(None)
        # Aggiungi il DataFrame alla lista
        dataframes.append(df)
    
    return dataframes, flag_failed


def read_table_url_selenium_xpath_nointestazione(url, xpaths): #funzion con selenium ma più lento
    # Utilizza il webdriver di Chrome con options per rendere il tutto più veloce
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-crash-reporter')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Attendi che la pagina si carichi completamente (puoi regolare il valore in base alle esigenze)
    driver.implicitly_wait(10)
    ### modo 1
    # # Ottieni il contenuto HTML dopo il rendering completo
    # response = driver.page_source

    # # Analizza l'HTML della pagina con BeautifulSoup
    # soup = BeautifulSoup(response, 'html.parser')

    # # Trova tutte le tabelle nella pagina con xpath specificato
    # tabelle=[]
    # dom = etree.HTML(str(soup))
    # for xpath in xpaths:
    #     tab_etree=dom.xpath(xpath)
    #     tab_html=etree.tostring(tab_etree[0])
    #     tab=BeautifulSoup(tab_html).find('table')
    #     tabelle.append(tab)

    ### modo 2
    # Trova tutte le tabelle nella pagina con xpath specificato
    tabelle=[]
    for i, xpath in enumerate(xpaths):
        try:
            tab=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute("outerHTML")
            # tab=driver.find_element(By.XPATH, xpath).get_attribute('innerHTML')
            tab=BeautifulSoup(tab)
            tabelle.append(tab)
        except:
            print('Xpath ' + str(i)+' non trovato')

    # Inizializza un elenco di DataFrame pandas
    dataframes = []
    # Itera attraverso le tabelle
    for tabella in tabelle:
        # Estrai i dati dalla tabella e crea un DataFrame pandas
        dati_tabella = []
        intestazioni = []

        righe = tabella.find_all('tr')
        for i, riga in enumerate(righe):
            celle = riga.find_all(['th', 'td'])
            riga_dati = []
            for cella in celle:
                riga_dati.append(cella.get_text().strip())
            dati_tabella.append(riga_dati)

        # Crea un DataFrame pandas
        df = pd.DataFrame(dati_tabella)
        df=df.set_index(0)
        df=df.rename_axis(None)
        # Aggiungi il DataFrame alla lista
        dataframes.append(df)
    driver.quit()
    return dataframes


def read_table_url_selenium_class_nointestazione(url, class_table): #funzion con selenium ma più lento
    # Utilizza il webdriver di Chrome con options per rendere il tutto più veloce
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-crash-reporter')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Attendi che la pagina si carichi completamente (puoi regolare il valore in base alle esigenze)
    driver.implicitly_wait(10)

    # Ottieni il contenuto HTML dopo il rendering completo
    response = driver.page_source

    # Analizza l'HTML della pagina con BeautifulSoup
    soup = BeautifulSoup(response, 'html.parser')

    # Trova tutte le tabelle nella pagina
    tabelle = soup.find_all('table', {"class": class_table})
    # Inizializza un elenco di DataFrame pandas
    dataframes = []
    # Itera attraverso le tabelle
    for tabella in tabelle:
        # Estrai i dati dalla tabella e crea un DataFrame pandas
        dati_tabella = []
        intestazioni = []

        righe = tabella.find_all('tr')
        for i, riga in enumerate(righe):
            celle = riga.find_all(['th', 'td'])
            riga_dati = []
            for cella in celle:
                riga_dati.append(cella.get_text().strip())
            dati_tabella.append(riga_dati)

        # Crea un DataFrame pandas
        df = pd.DataFrame(dati_tabella)
        df=df.set_index(0)
        df=df.rename_axis(None)
        # Aggiungi il DataFrame alla lista
        dataframes.append(df)
    return dataframes



def read_table_url_request_html_class_nointestazione(url, class_table): #funzion ma non in jupyter
    # # Fai una richiesta HTTP per ottenere il contenuto della pagina
    # response = requests.get(url)
    # # Analizza l'HTML della pagina con BeautifulSoup
    # soup = BeautifulSoup(response.text, 'html.parser')
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True)
    soup = BeautifulSoup(r.html.html,'html.parser')
    # Trova tutte le tabelle nella pagina
    tabelle = soup.find_all('table', {"class": class_table})
    # Inizializza un elenco di DataFrame pandas
    dataframes = []
    # Itera attraverso le tabelle
    for tabella in tabelle:
        # Estrai i dati dalla tabella e crea un DataFrame pandas
        dati_tabella = []
        intestazioni = []

        righe = tabella.find_all('tr')
        for i, riga in enumerate(righe):
            celle = riga.find_all(['th', 'td'])
            riga_dati = []
            for cella in celle:
                riga_dati.append(cella.get_text().strip())
            dati_tabella.append(riga_dati)

        # Crea un DataFrame pandas
        df = pd.DataFrame(dati_tabella)
        # Aggiungi il DataFrame alla lista
        dataframes.append(df)
    return dataframes

def read_table_url_isin(url, class_table):
    # Fai una richiesta HTTP per ottenere il contenuto della pagina
    response = requests.get(url)
    # Analizza l'HTML della pagina con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Trova tutte le tabelle nella pagina
    tabelle = soup.find_all('table', {"class": class_table})
    # Inizializza un elenco di DataFrame pandas
    dataframes = []
    # Itera attraverso le tabelle
    for tabella in tabelle:
        # Estrai i dati dalla tabella e crea un DataFrame pandas
        dati_tabella = []
        intestazioni = []

        righe = tabella.find_all('tr')
        for i, riga in enumerate(righe):
            if i==0:
                continue
            celle = riga.find_all(['th', 'td'])
            riga_dati = []
            for cella in celle:
                if i==1:
                    intestazioni.append(cella.get_text().strip())
                else:
                    riga_dati.append(cella.get_text().strip())
            if i>1:
                dati_tabella.append(riga_dati)

        # Crea un DataFrame pandas
        df = pd.DataFrame(dati_tabella, columns=intestazioni)
        #elaboro df
        df['Isin']=df['Isin'].apply(lambda x: x.split(' - ')[0])
        # Aggiungi il DataFrame alla lista
        dataframes.append(df)

    return dataframes