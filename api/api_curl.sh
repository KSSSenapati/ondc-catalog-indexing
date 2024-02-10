#!/bin/bash

input=$1

if [[ $input == "addProduct" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"productTitle": "Ponds"}' \
    http://localhost:8000/addProduct
fi


if [[ $input == "queryProduct" ]]; then
    curl -X PUT -H "Content-Type: application/json" \
    http://localhost:8000/queryProduct/1
fi


if [[ $input == "deleteProduct" ]]; then
    curl -X DELETE -H "Content-Type: application/json" \
    http://localhost:8000/deleteProduct/1
fi


if [[ $input == "updateAttributes" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"productId": "1", "discount": "2"}' \
    http://localhost:8000/updateAttributes
fi


if [[ $input == "updateDiscount" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"productId": "1", "discount": "2"}' \
    http://localhost:8000/updateDiscount
fi


if [[ $input == "updateSKU" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"productId": "1", "sizesCount": {"s": "2"}}' \
    http://localhost:8000/updateSKU
fi


if [[ $input == "updateRating" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"productId": "1", "rating": "4.4"}' \
    http://localhost:8000/updateRating
fi


if [[ $input == "updateTag" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"productId": "1", "acceleratorTag": "["new", "old"]"}' \
    http://localhost:8000/updateTag
fi


if [[ $input == "updateImage" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"productId": "1", "image": "/path/img.jpg"}' \
    http://localhost:8000/updateImage
fi


if [[ $input == "updateAd" ]]; then
    curl -X POST -H "Content-Type: application/json" \
    -d '{"productId": "1", "ad": "0"}' \
    http://localhost:8000/updateAd
fi