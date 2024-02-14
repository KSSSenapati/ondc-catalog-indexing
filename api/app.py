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
    product_id = message.get("product_id")
    main_image = message.get("main_image")
    if product_id is None or main_image is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="product_id and main_image fields are required")
    document = {
        "product_id": product_id, "main_image": main_image}
    result = collection.insert_one(document)


def tag_handler(message):
    collection = db["accelerator_tag"]
    product_id = message.get("product_id")
    accelerator_tag = message.get("accelerator_tag")
    if product_id is None or tag is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="product_id and accelerator_tag fields are required")
    document = {
        "product_id": product_id, "accelerator_tag": accelerator_tag}
    result = collection.insert_one(document)


def sku_handler(message):
    collection = db["sku"]
    product_id = message.get("product_id")
    sizesCount = message.get("sizesCount")
    if product_id is None or sizesCount is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="product_id and sizesCount fields are required")
    document = {
        "product_id": product_id, "sizesCount": sizesCount}
    result = collection.insert_one(document)


def price_handler(message):
    collection = db["price"]
    product_id = message.get("product_id")
    price = message.get("price")
    if price is None:
        return
    if product_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="product_id and price fields are required")
    document = {
        "product_id": product_id, "price": price}
    result = collection.insert_one(document)


kafka_map = {
    'updateAttribute': {'fields': ['attribute', 'handler': None]},
    'updateDiscount': {'fields': ['discount', 'sale_discount'], 'handler': None},
    'updateSKU': {'fields': ['sizesCount'], 'handler': sku_handler},
    'updateRating': {'fields': ['rating'], 'handler': None},
    'updateTag': {'fields': ['accelerator_tag'], 'handler': tag_handler},
    'updateAd': {'fields': ['ad_enabled'], 'handler': None},
    'updateImage': {'fields': ['main_image'], 'handler': image_handler},
    'updateProduct': {'fields': ['product_title', 'master_category', 'sub_category',
        'article', 'price', 'pincode'], 'handler': price_handler},
}


@app.post("/addProduct", status_code=status.HTTP_200_OK)
async def addProduct(request: Request):
    try:
        body = await request.json()

        if body.get('product_id') is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="product_id is required")

        body['product_id'] = '1234'
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
            raise raise HTTPException(
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
                opts['handler'](message)
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
