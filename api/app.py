from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer

import uvicorn
import pymongo
import pysolr
import json
import time


app = FastAPI()
producer = KafkaProducer(bootstrap_servers='localhost:9092')
solr = pysolr.Solr('http://localhost:8983/solr/ondc', timeout=10)
client = pymongo.MongoClient(host="localhost", port=27017, username="admin", password="admin")
db = client["lookup"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def image_handler(message):
    collection = db["image"]
    if message.get("main_image") is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="product_id is required")
    document = {
        "product_id": message["product_id"], "image_path": message["main_image"]}
    result = collection.insert_one(document)
    return str(result.inserted_id)


kafka_map = {
    'updateDiscount': {'fields': ['discount', 'sale_discount', 'discounted_price', 'sale_discounted_price'], 'handler': None},
    'updateSKU': {'fields': ['sizesCount'], 'handler': None},
    'updateRating': {'fields': ['rating'], 'handler': None},
    'updateTag': {'fields': ['accelerator_tag'], 'handler': None},
    'updateAd': {'fields': ['ad_enabled'], 'handler': None},
    'updateImage': {'fields': ['main_image'], 'handler': image_handler},
    'updateProduct': {'fields': ['product_title', 'master_category', 'sub_category',
        'article_type', 'attribute', 'price', 'pincode', 'attributes'], 'handler': None},
}


@app.post("/addProduct", status_code=status.HTTP_200_OK)
async def addProduct(request: Request):
    try:
        body = await request.json()

        if body.get('product_id') is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="product_id is required")

        body['product_id'] = body.get('product_id')
        producer.send('addProduct', value=json.dumps(body).encode('utf-8'))
        producer.flush()
        return {'status': 'success', 'message': 'Add successful'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/queryProduct", status_code=status.HTTP_200_OK)
async def queryProduct(request: Request):
    try:
        body = await request.json()
        if body.get('product_id') is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="product_id is required")

        query = 'id:"doc_{}"'.format(body.get('product_id'))
        results = solr.search(query)
        if len(results.docs):
            docs = results.docs[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Document not found")
        return {'status': 'success', 'message': docs}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/deleteProduct/{id}", status_code=status.HTTP_200_OK)
async def deleteProduct(id: str):
    try:
        if not id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="product_id is required")

        producer.send('deleteProduct', key=id.encode())
        producer.flush()
        return {'status': 'success', 'message': 'Delete successful'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/updateProduct", status_code=status.HTTP_200_OK)
async def updateProduct(request: Request):
    try:
        body = await request.json()

        if body.get('product_id') is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="product_id is required")
        for topic, opts in kafka_map.items():
            message = {key: body.get(key) for key in opts['fields'] if key in body}
            if not message:
                continue
            message['product_id'] = body.get('product_id')
            if opts['handler'] is not None:
                message['main_image'] = opts['handler'](message)
            producer.send(topic, value=json.dumps(message).encode('utf-8'))
            producer.flush()
        return {'status': 'success', 'message': 'Update successful'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Exception handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


# Other exception handling
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal server error"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
