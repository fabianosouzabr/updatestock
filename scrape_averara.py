from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import json
import time

url = 'https://www.girly.com.br'
apikey = 'd3d3e45cc44cdf02ecf8213180ba336e'
appkey = '2erarumEtubrUbrapeJaphEphekuph'


def login():
    driver = webdriver.Chrome('/home/fabiano/chromedriver')
    driver.get('http://www.averaraonline.com.br')
    driver.find_element(By.ID,'txtLoginEmail').send_keys('contato.girly@gmail.com')
    driver.find_element(By.ID,'txtLoginPassword').send_keys('girly2018', Keys.ENTER)
    #wait.until(EC.title_is('Home - AveRaraOnline'))
    return driver

def buscaestoque(driver,code):
    grade = dict()
    driver.get('http://www.averaraonline.com.br/produto/'+code)
    tabela=driver.find_element_by_xpath("//table[@id='fbits-produto-matriz-atributos']")    
    rows=tabela.find_elements_by_xpath(".//tr")
    tamanhos=rows[0].find_elements_by_xpath(".//th")
    qtdes=tabela.find_element_by_xpath("//tr/th/a[contains(@href,'-"+code+"/')]/../..")
    disp=qtdes.find_elements_by_xpath(".//td")
    for i in range(1,len(tamanhos)):
        x=tamanhos[i].text
        grade[x]=0 if disp[i-1].text=='Avise-me' else 1
    return grade

def atualizaestoque(productID, grade, tamdisp, url):
    header = {  'Content-Type': 'application/json',
                'X-API-KEY': apikey,
                'X-APP-KEY': appkey
             }
    data={"stock": []}
    request_url = url+'/api-v1/variants?product_id='+str(productID)
    response = requests.get(request_url, headers=header)
    for variation in response.json():
        for option in variation['option_values']:
            if option['option_name'] == 'Tamanho':
                print(variation['id']+' -> '+option['option_value_name']+' = '+str(grade[option['option_value_name']]))
                if option['option_value_name'] != tamdisp:
                    data['stock'].append({'variant_id':variation['id'],'quantity':grade[option['option_value_name']]})
                else:
                    print ('Valor não substituído: ' + option['option_value_name'] + ': qty(' + str(grade[option['option_value_name']]) + ') por já termos em estoque')
    request_url = url+'/api-v1/stock'
    bar = requests.put(request_url, headers=header, data=json.dumps(data))
    return bar

def getlistprod():
    listprod = {
        3899047:'75372',
        3902459:'75294',
        3881419:'75364',
        3812403:'75342',
        3821667:'75320',
        3902387:'75322',
        3849397:'75228',
        3902707:'75226',
        3838864:'75239',
        3902834:'75242',
        3902871:'75396',
        3838850:'75090',
        3902882:'75092',
        3902883:'75091',
        3902902:'75233',
        3902904:'75234',
        3838848:'75080',
        3838866:'75245',
        3905690:'75247',
        3905701:'75246',
        3905737:'74124',
        3905757:'74076',
        3843816:'73451',
        3905797:'73450',
        3881424:'75096',
        3881425:'75097',
        3838867:['75296','38'],
        3812304:['75363','38'],
        3881438:['75243','38'],
        3838862:['75235','38'],
        3843828:['74123','38'],
        3843803:['74077','38'],
        3838740:['75370','38']
    }
    return listprod

def main():
    testeAPI = False
    driver = login()
    listprod = getlistprod()
    for productID in listprod:
        if isinstance(listprod[productID],str):
            codforn = listprod[productID]
            tamdisp = None
        elif isinstance(listprod[productID],list):
            codforn = listprod[productID][0]
            tamdisp = str(listprod[productID][1])
        grade = buscaestoque(driver,codforn)
        print('-------------')
        print(productID)
        print(grade)
        atualizaestoque(productID, grade, tamdisp, url)

    input("pressione qualquer tecla para finalizar")

if __name__ == "__main__":
    main()

