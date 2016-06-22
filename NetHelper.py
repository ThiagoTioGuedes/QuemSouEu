# Exemplo bem simples de como trabalhar com a API da DropBox
# As configuracoes ja foram feitas no servidor da dropbox e o token
# de identificacao ja foi gerado

import dropbox
from random import randint 

token_validacao = 'rv7QP0_5jm4AAAAAAAAA47qM2pvueMuIRRKWe3P3isZz0yUr9Oaeoju0lnDXpWpE'

# Esse e o codigo token de validacao, importante mante-lo em seguranca
client = dropbox.client.DropboxClient(token_validacao)
print 'linked account: ', client.account_info()

f = open('working-draft.txt', 'w+')
f.write(str(randint(1,10000)));
f.close()
f = open('working-draft.txt', 'r')


response = client.put_file('/magnum-opus.txt', f, overwrite=True)
print 'uploaded: ', response

folder_metadata = client.metadata('/')
print 'metadata: ', folder_metadata

f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
out = open('magnum-opus.txt', 'wb')
out.write(f.read())
out.close()
print metadata