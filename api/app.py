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


@app.post("/addProduct", status_code=status.HTTP_200_OK)
async def addProduct(request: Request):
    try:
        body = await request.json()
        message = {
            "productTitle": body.get("productTitle"),
            "masterCategory": body.get("masterCategory"),
            "subCategory": body.get("subCategory"),
            "article": body.get("article"),
            "attribute": body.get("getAttributes"),
            "price": body.get("price"),
            "pinCode": body.get("pinCode"),
            "discount": body.get("discount"),
            "sizesCount": body.get("sizesCount"),
            "rating": body.get("rating"),
            "acceleratorTag": body.get("acceleratorTag"),
            "image": body.get("image"),
            "ad": body.get("ad"),
        }

        if body.get("productTitle") is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="productId is required")

        keys_to_remove = [key for key, val in message.items() if val is None]
        for key in keys_to_remove:
            message.pop(key)

        collection = db["product"]
        document = {"productTitle": message["productTitle"]}
        result = collection.insert_one(document)
        message["productId"] = str(result.inserted_id)

        producer.send('addProduct', value=json.dumps(message).encode('utf-8'))
        producer.flush()
        return {'status': 'success', 'message': 'New product added successfully'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.put("/queryProduct/{id}", status_code=status.HTTP_200_OK)
async def queryProduct(id: str, content: str):
    try:
        if not id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="productId is required")

        query = 'id:"doc_{}"'.format(id)
        results = solr.search(query)
        return {'status': 'success', 'message': results}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/deleteProduct/{id}", status_code=status.HTTP_200_OK)
async def deleteProduct(id: str):
    try:
        if not id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="productId is required")

        producer.send('deleteProduct', key=id.encode())
        producer.flush()
        return {'status': 'success', 'message': 'Product deleted successfully'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/updateAttributes", status_code=status.HTTP_200_OK)
async def updateAttributes(request: Request):
    try:
        body = await request.json()
        api_list = [updateDiscount, updateSKU,
                    updateRating, updateTag, updateImage, updateAd]
        for api in api_list:
            try:
                api(request)
            except Exception as e:
                print(f"Exception in {api.__name__}: {e}")
                pass

        message = {
            "productId": body.get("productId"),
            "productTitle": body.get("productTitle"),
            "masterCategory": body.get("masterCategory"),
            "subCategory": body.get("subCategory"),
            "article": body.get("article"),
            "attribute": body.get("getAttributes"),
            "price": body.get("price"),
            "pinCode": body.get("pinCode"),
        }

        keys_to_remove = [key for key, val in message.items() if val is None]
        for key in keys_to_remove:
            message.pop(key)

        producer.send('updateAttributes', value=json.dumps(
            message).encode('utf-8'))
        producer.flush()
        return {'status': 'success', 'message': 'Attributes updated successfully'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/updateDiscount", status_code=status.HTTP_200_OK)
async def updateDiscount(request: Request):
    try:
        body = await request.json()
        message = {
            "productId": body.get("productId"),
            "discount": body.get("discount"),
            "salesDiscount": body.get("salesDiscount"),
        }

        if message["salesDiscount"] is None:
            message["salesDiscount"] = 0
        print(message)
        for key, val in message.items():
            if val is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} is required")

        producer.send('updateDiscount', value=json.dumps(
            message).encode('utf-8'))
        producer.flush()
        return {'status': 'success', 'message': 'Discount updated successfully'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/updateSKU", status_code=status.HTTP_200_OK)
async def updateSKU(request: Request):
    try:
        body = await request.json()
        message = {
            "productId": body.get("productId"),
            "sizesCount": body.get("sizesCount"),
        }

        for key, val in message.items():
            if val is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} is required")

        producer.send('updateSKU', value=json.dumps(message).encode('utf-8'))
        producer.flush()
        return {'status': 'success', 'message': 'SKU updated successfully'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/updateRating", status_code=status.HTTP_200_OK)
async def updateRating(request: Request):
    try:
        body = await request.json()
        message = {
            "productId": body.get("productId"),
            "rating": body.get("rating"),
        }

        for key, val in message.items():
            if val is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} is required")

        producer.send('updateRating', value=json.dumps(
            message).encode('utf-8'))
        producer.flush()
        return {'status': 'success', 'message': 'Data pushed to Kafka successfully.'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/updateTag", status_code=status.HTTP_200_OK)
async def updateTag(request: Request):
    try:
        body = await request.json()
        message = {
            "productId": body.get("productId"),
            "acceleratorTag": body.get("acceleratorTag"),
        }

        for key, val in message.items():
            if val is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} is required")

        producer.send('updateTag', value=json.dumps(message).encode('utf-8'))
        producer.flush()
        return {'status': 'success', 'message': 'Tag updated successfully'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/updateImage", status_code=status.HTTP_200_OK)
async def updateImage(request: Request):
    try:
        body = await request.json()
        message = {
            "productId": body.get("productId"),
            "image": body.get("image"),
        }

        for key, val in message.items():
            if val is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} is required")

        collection = db["image"]
        document = {
            "productId": message["productId"], "imagePath": message["image"]}
        result = collection.insert_one(document)

        message["imageId"] = str(result.inserted_id)
        message.pop('image')

        producer.send('updateImage', value=json.dumps(message).encode('utf-8'))
        producer.flush()
        return {'status': 'success', 'message': 'Image updated successfully'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/updateAd", status_code=status.HTTP_200_OK)
async def updateAd(request: Request):
    try:
        body = await request.json()
        message = {
            "productId": body.get("productId"),
            "ad": body.get("ad"),
        }

        for key, val in message.items():
            if val is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} is required")

        producer.send('updateAd', value=json.dumps(message).encode('utf-8'))
        producer.flush()
        return {'status': 'success', 'message': 'Tag updated successfully'}
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
