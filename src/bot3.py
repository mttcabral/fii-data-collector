from bot2 import get_fii_code_list
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from date import get_period
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

"""
# This bot will collect the proceeds
# Note: The translation (Portuguese (provento) -> English  (proceeds)) might
# not be very accurate
#
# The main logic is from Pedro Lucas Paulino
# GitHub link: https://github.com/PLPaulino
"""

# The following code was take from a co-worker (Pedro Lucas Paulino), therefore
# it's in Portuguese, the code will be refactored to English afterwards


def bot3():
    fiis = get_fii_code_list()
    print(execucao_tudo(fiis[2]))


def execucao_tudo(nome):
    option = Options()
    option.headless = True

    try:
        browser = webdriver.Firefox(options=option)

        # definindo datas inicias e finais para ser parâmentros de execução referente ao bot1
        datas = get_period()
        data_inicial = datas[0]
        data_final = datas[1]

        # executando o bot1 e alocando os dados recebidos em uma variável
        dados_bot1 = get_dados(data_inicial, data_final, nome, browser)

        return dados_bot1

    except:
        print("Erro! Falha ao concluir o scraping.")

    finally:
        browser.quit()


def get_dados(data_inicial, data_final, nome, browser):

    print(f"\n\nNome: {nome}")

    try:
        """
        # Function: efetuar_pesquisa
        """
        data_final_format = data_final.split(
            '/')[2] + '-' + data_final.split('/')[1] + '-' + data_final.split('/')[0]
        data_inicial_format = data_inicial.split(
            '/')[2] + '-' + data_inicial.split('/')[1] + '-' + data_inicial.split('/')[0]

        url = f'https://sistemasweb.b3.com.br/PlantaoNoticias/Noticias/ListarTitulosNoticias?agencia=18&palavra={nome}&dataInicial={data_inicial_format}&dataFinal={data_final_format}'
        browser.get(url)

        arquivo_json = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body")))
        html_arquivo_json = arquivo_json.get_attribute('outerHTML')
        soup_json = BeautifulSoup(html_arquivo_json, 'html.parser')
        list_dicionarios_noticia = json.loads(soup_json.text)
        """
        # END
        """

        """
        # Function: encontrar_credenciais_noticia_qualificada
        """
        credenciais = []
        identificador = "Aviso aos Cotistas"

        lista_dic_qualificado = (list(filter(lambda dicionario: identificador in str(
            dicionario['NwsMsg']['headline']), list_dicionarios_noticia)))

        for x in range(len(lista_dic_qualificado)):
            if (lista_dic_qualificado[x]['NwsMsg']['headline'][-2] == 'N'):
                incremento_id = lista_dic_qualificado[x]['NwsMsg']['id']
                break

        incremento_data_noticia = lista_dic_qualificado[-1]['NwsMsg']['dateTime']

        credenciais.append(incremento_id)
        credenciais.append(incremento_data_noticia)
        credenciais_noticia = credenciais
        """
        # END
        """

        """
        # Function: solicitar_noticia_qualificada
        """
        url = f'https://sistemasweb.b3.com.br/PlantaoNoticias/Noticias/Detail?idNoticia={credenciais_noticia[0]}&agencia=18&dataNoticia={credenciais_noticia[1]}'
        browser.get(url)

        # selecionado o conteúdo html da pagina de notícia encotrada
        link = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "conteudoDetalhe")))
        html_link = link.get_attribute('outerHTML')
        soup_link = BeautifulSoup(html_link, 'html.parser')
        """
        # END
        """

        """
        # Function: encontrar_id__url_tabela
        """
        for ancora in soup_link.findAll('a'):
            lista_link = str(ancora['href']).split('=')
            id_tabela = lista_link[1]

        url_tabela = 'https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=' + \
            id_tabela+'&#toolbar=0'
        """
        # END
        """

        #
        #
        #
        browser.get(url_tabela)
        # a partir do 'xpath' encotra-se a tabela e logo em seguida é armazenada em uma variável
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/table[2]')))

        tabela = browser.find_element(By.XPATH, '/html/body/table[2]')
        text_para_testar = browser.find_element(
            By.XPATH, '/html/body/table[1]/tbody/tr[4]/td[4]')

        # extrai o html da tabela que logo em seguida é retornado pela função
        html_tabela = tabela.get_attribute('outerHTML')
        soup_tabela = BeautifulSoup(html_tabela, 'html.parser')
        #
        #
        #

        """
        # Function: formata_tabela_bot1
        """
        soup_dados = []

        # solicitando os dados no interior da tabela
        for span in soup_tabela.findAll('span', class_='dado-valores'):
            soup_dados.append(span.text)
        """
        # END
        """

        # acrescenta '11' ao final do nome do fiis
        nome_formato_11 = (str(nome + "11"))

        # test
        htmml = text_para_testar.get_attribute('outerHTML')
        soup_tabela2 = BeautifulSoup(htmml, 'html.parser')
        if (soup_tabela2.get_text() == nome_formato_11):
            print("AIAIAI")
        #
        """
        # Function: formata_valor_provento
        """
        string_valor_provento = soup_dados[5].split(',')
        valor_provento = float(
            string_valor_provento[0] + '.' + string_valor_provento[1])
        """
        # END
        """

        valor_provento = {nome: valor_provento}

        return valor_provento

    except():
        print("Erro de execução!!!")

    finally:
        print(f"{nome}: Processo de tentativa finalisado.")


bot3()
