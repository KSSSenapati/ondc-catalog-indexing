#!/bin/bash

input=$1

if [[ $input == "addProduct" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"product_id":"10001", "product_title": "Ponds"}' \
    http://localhost:8000/addProduct
fi


if [[ $input == "queryProduct" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"product_id": "123"}' \
    http://localhost:8000/queryProduct
fi


if [[ $input == "deleteProduct" ]]; then
    curl -X DELETE -H "Content-Type: application/json" \
    http://localhost:8000/deleteProduct/doc_1234
fi


if [[ $input == "updateProduct" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"product_id": "1234", "product_title": "ponds cream"}' \
    http://localhost:8000/updateProduct
fi


if [[ $input == "updateDiscount" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"product_id": 1, "discount": 2}' \
    http://localhost:8000/updateProduct
fi


if [[ $input == "updateSKU" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"product_id": 1234, "sizesCount": {"s": 1, "m": 3}}' \
    http://localhost:8000/updateProduct
fi


if [[ $input == "updateRating" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"product_id": "1234", "rating": 4.4}' \
    http://localhost:8000/updateProduct
fi


if [[ $input == "updateTag" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"product_id": 1, "accelerator_tag": ["new"]}' \
    http://localhost:8000/updateProduct
fi


if [[ $input == "updateImage" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"product_id": 1, "main_image": "/path/img.jpg"}' \
    http://localhost:8000/updateProduct
fi


if [[ $input == "updateAd" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"product_id": 1, "ad_enabled": 0}' \
    http://localhost:8000/updateProduct
fi