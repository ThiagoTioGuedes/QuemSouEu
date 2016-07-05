# Exemplo bem simples de como trabalhar com a API da DropBox
# As configuracoes ja foram feitas no servidor da dropbox e o token
# de identificacao ja foi gerado

import dropbox
from random import randint 
import os

token_validacao = 'rv7QP0_5jm4AAAAAAAAA47qM2pvueMuIRRKWe3P3isZz0yUr9Oaeoju0lnDXpWpE'
client = dropbox.client.DropboxClient(token_validacao)

# print 'linked account: ', client.account_info()
# f = open('working-draft.txt', 'w+')
# f.write(str(randint(1,10000)));
# f.close()
# folder_metadata = client.metadata('/')
# print 'metadata: ', folder_metadata

def baixar_banco_bibliotecas():
    f = client.get_file('Bibliotecas/banco_bibliotecas.xml')    
    out = open('Bibliotecas'+os.sep+'banco_bibliotecas.xml', 'wb')
    out.write(f.read())
    out.close()

# Ainda nao colocada em uso; Talvez para uma versao futura
def enviar_biblioteca(nome_biblioteca):
    f = open('Bibliotecas'+os.sep+nome_biblioteca+'.xml', 'r')
    return client.put_file('Bibliotecas/'+nome_biblioteca+'.xml', f, overwrite=True)

def baixar_biblioteca(nome_biblioteca):
    f = client.get_file('Bibliotecas/'+nome_biblioteca+'.xml')
    out = open('Bibliotecas'+os.sep+nome_biblioteca+'.xml', 'wb')
    out.write(f.read())
    out.close()