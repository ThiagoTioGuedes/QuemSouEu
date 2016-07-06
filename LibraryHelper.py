import NetHelper

__author__ = 'Thiago'
import xml.etree.cElementTree as ET
import os
from xml.dom.minidom import parse, Node

# Caminho dado para funcionar no android
pasta_base = "/sdcard/download/"


def abrir_arquivo_banco_bibliotecas():
    # Aqui abrimos o arquivo XML que lista todas as bibliotecas presentes no
    # servidor, ja foi previamente baixado, usando o minidom parser
    domtree = parse(pasta_base+'Bibliotecas'+os.sep+'banco_bibliotecas.xml')
    collection = domtree.documentElement

    tmpRetorno = []
    # Pega todas as bibliotecas que foram cadastradas no servidor
    for item in collection.getElementsByTagName("Biblioteca"):
        tmpRetorno.append(str(item.firstChild.nodeValue))

    return tmpRetorno
    
    

def lista_bibliotecas():
    return tratar_nomes_biliotecas(os.listdir(pasta_base+'Bibliotecas'));
    

def abrir_arquivo_biblioteca(nome_arquivo):
    # Aqui abrimos o arquivo XML usando o minidom parser
    domtree = parse(pasta_base+'Bibliotecas'+os.sep+nome_arquivo+".xml")
    collection = domtree.documentElement

    tmpRetorno = []
    # Pega todos os itens que foram cadastrados
    for item in collection.getElementsByTagName("Item"):
        tmpRetorno.append(item.firstChild.nodeValue)

    return tmpRetorno
# Nao usado, mesmo funcionando
# def adicionar_biblioteca(nome_biblioteca):
#     domtree = parse(pasta_base+'Bibliotecas'+os.sep+'banco_bibliotecas.xml')

#     novo_no = domtree.createElement("Biblioteca")
#     txt = domtree.createTextNode(nome_biblioteca)
#     novo_no.appendChild(txt)
#     domtree.childNodes[0].appendChild(novo_no)

#     domtree.toxml()
#     domtree.unlink()

#     NetHelper.enviar_biblioteca(nome_biblioteca)
#     NetHelper.enviar_biblioteca("banco_bibliotecas")


def criar_arquivo(nome_arquivo, lista_itens=[]):
    root = ET.Element(nome_arquivo)

    for item in lista_itens:
        ET.SubElement(root, "Item").text = item

    ET.ElementTree(root).write(pasta_base+'Bibliotecas'+os.sep+ nome_arquivo + ".xml")


# metodos uteis
def criar_pasta_bibliotecas():
    if not os.path.exists(pasta_base+'Bibliotecas'):
        os.makedirs(pasta_base+'Bibliotecas')
        
def tratar_nomes_biliotecas(lista):
    tmp_lista = []

    for bib in lista:
        bib = bib.replace('.xml', '')
        # Para que nao liste por engano o arquivo que lista as bibliotecas
        if not bib == 'banco_bibliotecas':
            tmp_lista.append(bib)

    return tmp_lista

# por ser um xml, se a biblioteca tiver espacos a leitura de seu arquivo dara problema
def tratar_nome_biblioteca(nome_biblioteca):
    return nome_biblioteca.replace(' ', '_');