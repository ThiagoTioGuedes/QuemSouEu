__author__ = 'Thiago'
import xml.etree.cElementTree as ET
import os
from xml.dom.minidom import parse

def lista_bibliotecas():
    return tratar_nomes_biliotecas(os.listdir('Bibliotecas'));


def criar_pasta_bibliotecas():
    if not os.path.exists('Bibliotecas'):
        os.makedirs('Bibliotecas')


def abrir_arquivo_biblioteca(nome_arquivo):
    # Aqui abrimos o arquivo XML usando o minidom parser
    domtree = parse('Bibliotecas\\'+nome_arquivo+".xml")
    collection = domtree.documentElement

    # Pega todos os itens que foram cadastrados
    return collection.getElementsByTagName("Item")


def criar_arquivo(nome_arquivo, lista_itens=[]):
    root = ET.Element(nome_arquivo)

    for item in lista_itens:
        ET.SubElement(root, "Item").text = item

    ET.ElementTree(root).write('Bibliotecas\\'+ nome_arquivo + ".xml")

def tratar_nomes_biliotecas(lista):
    tmp_lista = []

    for bib in lista:
        bib = bib.replace('.xml', '')
        tmp_lista.append(bib)

    return tmp_lista