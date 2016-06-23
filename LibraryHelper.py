__author__ = 'Thiago'
import xml.etree.cElementTree as ET
import os
from xml.dom.minidom import parse



def abrir_arquivo_banco_bibliotecas():
    # Aqui abrimos o arquivo XML que lista todas as bibliotecas presentes no
    # servidor, já foi previamente baixado, usando o minidom parser
    domtree = parse('Bibliotecas\\banco_bibliotecas.xml')
    collection = domtree.documentElement

    tmpRetorno = []
    # Pega todas as bibliotecas que foram cadastradas no servidor
    for item in collection.getElementsByTagName("Biblioteca"):
        tmpRetorno.append(item.firstChild.nodeValue)

    return tmpRetorno
    
    

def lista_bibliotecas():
    return tratar_nomes_biliotecas(os.listdir('Bibliotecas'));

def abrir_arquivo_biblioteca(nome_arquivo):
    # Aqui abrimos o arquivo XML usando o minidom parser
    domtree = parse('Bibliotecas\\'+nome_arquivo+".xml")
    collection = domtree.documentElement

    tmpRetorno = []
    # Pega todos os itens que foram cadastrados
    for item in collection.getElementsByTagName("Item"):
        tmpRetorno.append(item.firstChild.nodeValue)

    return tmpRetorno


def criar_arquivo(nome_arquivo, lista_itens=[]):
    root = ET.Element(nome_arquivo)

    for item in lista_itens:
        ET.SubElement(root, "Item").text = item

    ET.ElementTree(root).write('Bibliotecas\\'+ nome_arquivo + ".xml")


# metodos uteis
def criar_pasta_bibliotecas():
    if not os.path.exists('Bibliotecas'):
        os.makedirs('Bibliotecas')
        
def tratar_nomes_biliotecas(lista):
    tmp_lista = []

    for bib in lista:
        bib = bib.replace('.xml', '')
        tmp_lista.append(bib)

    return tmp_lista

# por ser um xml, se a biblioteca tiver espacos a leitura de seu arquivo dara problema
def tratar_nome_biblioteca(nome_biblioteca):
    return nome_biblioteca.replace(' ', '_');