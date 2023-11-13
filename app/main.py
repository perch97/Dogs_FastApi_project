from enum import Enum
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from typing import List, Union,Optional
from datetime import datetime
app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

fake_dogs = {
    0:'dog1',
    1:'dog2'
}

# ------------- GET/ Root -------------#
@app.get('/')
async def root():
    return {'status': 200, 'data':"string"}

# ------------- POST /post GET Post -------------#

@app.post('/post')
def post_time(input_timestamp:Timestamp = None):
    new_id = max([time_stamp.id for time_stamp in post_db ])+1
    if input_timestamp:
        post_db.append(input_timestamp)
    else:
        new_timestamp = Timestamp(id=new_id,timestamp=int(datetime.now().timestamp()))
        post_db.append(new_timestamp)
    return post_db[-1]

# ------------- GET /dog GET Dogs -------------#


@app.get('/dog',response_model = List[Dog])
def get_dog(kind:DogType = ''):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return []

# ------------- POST /dog Create Dog -------------#
@app.post('/dog')
def create_dog(dog:Dog):
    dogs_db[len(dogs_db)] = dog

# ------------- GET /dog/{pk} Get Dog By Pk -------------#

@app.get('/dog/{pk}',response_model = List[Dog])
def get_dog(pk:int):
    if pk>=0:
        return [dog for dog in dogs_db.values() if dog.pk == pk]
    

# ------------- PATCH /dog/{pk} Update Dog-------------#
router = APIRouter()

@app.patch("/dog/{pk}")
def update_dog( pk: int ,dog : Dog):
    item_id = [id for id in dogs_db.keys() if dogs_db[id].pk==pk][0]
    dogs_db[item_id]=dog
    return dogs_db



