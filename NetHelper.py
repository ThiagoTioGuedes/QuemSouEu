# Exemplo bem simples de como trabalhar com a API da DropBox
# As configuracoes ja foram feitas no servidor da dropbox e o token
# de identificacao ja foi gerado

import dropbox

client = dropbox.client.DropboxClient('rv7QP0_5jm4AAAAAAAAA47qM2pvueMuIRRKWe3P3isZz0yUr9Oaeoju0lnDXpWpE')
print 'linked account: ', client.account_info()

f = open('working-draft.txt', 'w+')
response = client.put_file('/magnum-opus.txt', f)
print 'uploaded: ', response

folder_metadata = client.metadata('/')
print 'metadata: ', folder_metadata

f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
out = open('magnum-opus.txt', 'wb')
out.write(f.read())
out.close()
print metadata