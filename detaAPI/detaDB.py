# 1) pip install deta
from deta import Deta

# 2) initialize with a project key
deta = Deta("b0l9wzou_5GKoiQu3uNUc4Qe1Q86yNkHavvseRDYX")

# 3) create and use as many DBs as you want!
users = deta.Base("contactos")

users.insert({
    "id_contacto":1,
    "nombre": "Jesus",
    "email": "jesus@gmail.com",
    "telefono":"3456789678"
})

fetch_res = users.fetch({"nombre": "Jesus"})
