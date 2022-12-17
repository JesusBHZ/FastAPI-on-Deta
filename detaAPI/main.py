from fastapi import FastAPI
from pydantic import BaseModel
from deta import Deta
from pydantic import EmailStr
from typing import List
from fastapi.responses import JSONResponse
from fastapi import HTTPException,status


deta = Deta()
contact = deta.Base("contacto")

app = FastAPI()

# Modelo de respuesta Mensaje
class Mensaje(BaseModel):
    mensaje:str
    
# Moelo de respuesta Contacto   
class Contacto(BaseModel):
    id_contacto: int
    nombre : str
    email : EmailStr
    telefono: str
    
# Modelo ContactoIn
# Verbos: POST, PUT
class ContactoIN(BaseModel):
    id_contacto: int
    nombre:str
    email:EmailStr
    telefono:str
    
description = """
 # Contactos API REST
 ---
 > Implementacion de una API REST con conexion a bases de datos para realizar un CRUD a la tabla contactos
 """
 
app = FastAPI(
 description=description,
 version="0.0.1",
 terms_of_service="http/example.com/terms/",
 contact={
     "name":"Jesus BHZ",
     "url":"https://github.com/JesusBHZ",
 },
 license_info={
     "name":"Apache 2.0",
     "url":"https://www.apache.org/licenses/LICENSE-2.0.html"
 },)



# Metodo GET para RAIZ
@app.get(
    "/",
    response_model = Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Endpoint principal",
    description = "Regresa un mensaje de Bienvenida"
    )
async def read_root():
    response = {"mensaje":"Holaaa a todos"}
    return response


# Metodo GET para consultar todos los datos
@app.get(
    "/contactos/", 
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Lista de contactos",
    description="Endpoint que regrese un array con todos los contactos"
   )
async def get_contactos():
    try:
        res = contact.fetch()
        return res
    except Exception as error:
        print(f"Error en get.contactos {error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "ERROR al consultar datos"
        )

 
 
# Metodo GET para consultar un solo dato
@app.get(
    "/contactos/{key}",
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Un solo contacto",
    description="Endpoint que regrese un array con todos los contactos"
   )
def get_contactos(key: str):
    try:
        res = contact.get(key)
        if res:
            return res
        else:
            return JSONResponse(status_code=404, content={"message":"El id de ese contacto no existe"})
    except Exception as error:
        print(f"Error en get.contactos {error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "ERROR al consultar datos"
        )
 

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.post(
    "/contacto/",
    response_model = Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Inserta un contacto",
    description = "Metodo para insertar un nuevo contacto"
    )
def create_contact(contacto: ContactoIN):
    try:
        if len(contacto.telefono) <10:
            return JSONResponse(status_code=404, content={"message":"El numero de telefono debe tener 10 caracteres"})
        else:
            if contacto.telefono.isdigit() == True:
                u = contact.put(contacto.dict())
                return JSONResponse(status_code=202, content={"message":"Contacto insertado"})
            else:
                return JSONResponse(status_code=404, content={"message":"El numero no tiene el formato correcto"})                
    except Exception as error:
        print(f"Error en get.contactos {error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "ERROR al insertar los datos"
        )


# Metodo PUT para modificar un contacto     
@app.put(
    "/contactos/{key}",
    response_model = Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Modifica un contacto",
    description = "Metodo para modificar un contacto"
    )
def create_contact(contacto: ContactoIN, key: str):
    try:
        if len(contacto.telefono) <10:
            return JSONResponse(status_code=404, content={"message":"El numero de telefono debe tener 10 caracteres"})
        else:
            if contacto.telefono.isdigit() == True:
                res = contact.get(key)
                if res:
                    user = contact.put(contacto.dict(), key)
                    return JSONResponse(status_code=202, content={"message":"Contacto modificado con exito"})
                else:
                    return JSONResponse(status_code=404, content={"message":"El id de ese contacto no existe"})
            else:
                return JSONResponse(status_code=404, content={"message":"El numero no tiene el formato correcto"})                
    except Exception as error:
        print(f"Error en get.contactos {error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "ERROR al insertar los datos"
        )
    


# Metodo DELETE para eliminar un contacto     
@app.delete(
    "/contactos/{key}",
    response_model = Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Eliminar un contacto",
    description="Endpoint que elimina un contacto"
    )
async def delete_contacto(key: str):
    res = contact.get(key)
    if res:
        contact.delete(key)
        return JSONResponse(status_code=202, content={"message":"Contacto eliminado con exito"})
    else:
        return JSONResponse(status_code=404, content={"message":"El id de ese contacto no existe"})