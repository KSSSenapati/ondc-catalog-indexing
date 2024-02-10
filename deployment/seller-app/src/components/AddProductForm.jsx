import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Col } from 'react-bootstrap';
import { Row }from 'react-bootstrap';
import { ImageUpload } from './ImageUpload';
import { useState } from 'react';
import Table from "react-bootstrap/Table";
import { TagsInput } from 'react-tag-input-component';

import data from '../data.json';
import ShowModal from './ShowModal';

import '../config.js';

var randomize = require('randomatic');

function AddProductForm() {
  const [productId, setProductId] = useState("")
  const [productTitle, setProductTitle] = useState("")

  const [productType, setProductType] = useState("")

  const masterCategoryList = Object.keys(data);
  const [subCategoryList, setSubCategoryList] = useState([])
  const [articleList, setArticleList] = useState([])

  const [masterCategory, setMasterCategory] = useState("")
  const [subCategory, setSubCategory] = useState("")
  const [article, setArticle] = useState("")

  const [attribute, setAttribute] = useState([])
  const [attributeValue, setAttributeValue] = useState([])

  const [imageFile, setImageFile] = useState()

  const [price, setPrice] = useState(0)
  const [discount, setDiscount] = useState(0)
  const [discountedPrice, setDiscountedPrice] = useState(0)

  const [acceleratorTag, setAcceleratorTag] = useState([])
  const [pinCode, setPinCode] = useState([])

  const [submitStatus, setSubmitStatus] = useState(false)

  const handleAttributeChange = (index, value) => {
    const updateValue = [...attributeValue];
    updateValue[index] = value;
    setAttributeValue(updateValue);
  }

  const getAttributes = () => {
    const _attribute = {};
    attribute.forEach((item, index) => {
      if (attributeValue[index] !==  undefined) {
        
        _attribute[item] = attributeValue[index];
      }
    })
    return _attribute;
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    setProductId(randomize('A0', 12));
    const _payload = {
      "product_id": productId,
      "product_title": productTitle,
      "product_type": productType,
      "master_category": masterCategory,
      "sub_category": subCategory,
      "article_type": article,
      "attributes": getAttributes(),
      "price": price,
      "discount": discount,
      "discounted_price": discountedPrice,
      "accelerator_tag": acceleratorTag,
      "pincode": pinCode,
      "main_image" : imageFile
    }
    setSubmitStatus(true);
    const options = {
      method: 'post',
      headers: {
        "access-control-allow-origin" : "*",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(_payload)
    }

    console.log(options.body);
    fetch(global.config.url+"addProduct", options)
      .then(response => response.json())
      .then(response => console.log(response))
      .catch(err => console.log(err))
  }

  const handleHierarchy = (option, e) => {
    switch(option){
      case 0:
        setAttribute([]);
        setAttributeValue([]);
        break;
      case 1:
        setAttribute([]);
        setAttributeValue([]);
        setArticle("");
        setArticleList([])
        break;
      case 2:
        setAttribute([]);
        setAttributeValue([]);
        setArticle("");
        setArticleList([])
        setSubCategory("");
        setSubCategoryList([]);
        break;
      case 3:
        setSubCategoryList(Object.keys(data[e.target.value]));
        // setSubCategory("");
        // setArticle("");
        // setAttribute([]);
        // if (subCategory !== "" ) setArticleList(Object.keys(data[e.target.value][subCategory]));
        // if (article !== "") setAttribute(data[e.target.value][subCategory][article]);
        break
      default:
        return 0;
    }
  }

  return (
    <Form onSubmit={(e) => handleSubmit(e)} className="pb-6">
      {submitStatus && <ShowModal modalContent={`Your Product id is ${productId}`} onClose={()=> setSubmitStatus(false)} modalShow={submitStatus} modalTitle="Successful Product Addition" />}
        <Row>
        <h3 className='mb-3'>Add Product Form</h3>
        <Col md = {8}>
            <Row>
              <Col md={8}>
                <Form.Group className="mb-3" controlId="formProductTitle">
                    <Form.Label>Product Title</Form.Label>
                    <Form.Control required type="text" placeholder="Enter Title" onChange={e => setProductTitle(e.target.value)}/>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="mb-3" controld="formMasterCategory" >
                    <Form.Label>Set Product Type</Form.Label>
                    <Form.Select required onChange={(e) => setProductType(e.target.value)}>
                      <option></option>
                      <option>Live</option>
                      <option>Non-Live</option>
                    </Form.Select>
                  </Form.Group>
              </Col>
            </Row>

            {/* Master Category Dropdown Start*/}
            <Row>
              <Col>
                  <Form.Group className="mb-3" controld="formMasterCategory" >
                    <Form.Label>Set Master Category</Form.Label>
                    <Form.Select required disabled={productTitle===""} onChange={(e) => {
                        setMasterCategory(e.target.value);
                        e.target.value === "" ? handleHierarchy(2, e) : handleHierarchy(3, e);
                      }
                    }>
                      <option></option>
                      {masterCategoryList.map((item, index)=> {
                        return(
                          <>
                          <option key={index}>{item}</option>
                          </>
                        )
                      })}
                    </Form.Select>
                  </Form.Group>
              </Col>
              {/* Master Category Dropdown End*/}

              {/* Sub category Dropdown Start*/}
              <Col>
                  <Form.Group className="mb-3" controld="formSubCategory" >
                    <Form.Label>Set Sub Category</Form.Label>
                    <Form.Select required disabled={subCategoryList.length===0} onChange={(e) => {
                        setSubCategory(e.target.value);
                        e.target.value === "" ? handleHierarchy(1, e) : setArticleList(Object.keys(data[masterCategory][e.target.value]));
                      }
                    }>
                      <option></option>
                      {subCategoryList.length!== 0 && subCategoryList.map((item, index)=> {
                        return(
                          <>
                          <option key={index}>{item}</option>
                          </>
                        )
                      })}
                    </Form.Select>
                  </Form.Group>
              </Col>
              {/* Sub category Dropdown End*/}

              {/* Article Dropdown Start*/}
              <Col>
                  <Form.Group className="mb-3" controld="formArticle" >
                    <Form.Label>Set Article</Form.Label>
                    <Form.Select required disabled={articleList.length===0} onChange={(e) => {
                      setArticle(e.target.value);
                      if (e.target.value !== "") {
                        const list_ = data[masterCategory][subCategory][e.target.value]
                        setAttribute(list_);
                        setAttributeValue(new Array(list_.length))
                      } else {
                        handleHierarchy(0, e)
                      }
                    }
                    }>
                      <option></option>
                      {articleList.length!== 0 && articleList.map((item, index)=> {
                        return(
                          <>
                          <option key={index}>{item}</option>
                          </>
                        )
                      })}
                    </Form.Select>
                  </Form.Group>
              </Col>
              {/* Article Dropdown End*/}
            </Row>

            {/* Attribute List Start */}
            <Row>
              {attribute.length !== 0 && 
                <Table bordered hover>
                  <thead>
                    <tr style={{textAlign: "center"}}>
                      <th>Attributes</th>
                      <th>Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {attribute.map((item, index) => {
                      return(
                        <tr>
                          <td>
                            {item.charAt(0).toUpperCase() + item.slice(1)}
                          </td>
                          <td>
                            <Form.Control type="text" key ={index} value={attributeValue[index]} onChange={(e) => handleAttributeChange(index, e.target.value)} />
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </Table>
              }
            </Row>
            {/* Attribute List End */}

            <Row>
              <Col>
                <Form.Group className="mb-3" controlId="formPrice">
                    <Form.Label>Price</Form.Label>
                    <Form.Control required type="number" min="0" placeholder="Enter Price" onChange={(e) => {
                      const val_ = e.target.value;
                      setPrice(val_);
                      if (discount !== 0) setDiscountedPrice((1-(0.01 * discount))* val_);
                      }
                    }/>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="mb-3" controlId="formDiscount">
                    <Form.Label>Discount (%) </Form.Label>
                    <Form.Control type="number" disabled={price==="0"} min="0" max="100" value={discount} placeholder="Enter Discount(%)" onChange={(e) => {
                      setDiscount(e.target.value);
                      setDiscountedPrice((1-(0.01 * e.target.value))* price);
                      }
                    }/>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="mb-3" controlId="formDiscountedPrice">
                    <Form.Label>Discounted Price (INR) </Form.Label>
                    <Form.Control type="number" disabled={price==="0"} min="0" value={discountedPrice} placeholder="Enter Discounted Price (INR)" onChange={(e) => {
                      setDiscountedPrice(e.target.value);
                      setDiscount((1 - e.target.value/price) * 100);
                      }
                    }/>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col>
              <Form.Group className="mb-3" controlId="formAcceleratorTag">
                  <Form.Label>Accelerator Tags</Form.Label>
                  <TagsInput
                    value={acceleratorTag}
                    onChange={setAcceleratorTag}
                    name="Accelerator"
                    placeHolder="Enter Accelerator Tags"
                  />
              </Form.Group>
              </Col>
              <Col>
              <Form.Group className="mb-3" controlId="formPincode">
                  <Form.Label>Pincode</Form.Label>
                  <TagsInput
                    value={pinCode}
                    onChange={setPinCode}
                    name="pincode"
                    placeHolder="Enter Pincodes"
                  />
              </Form.Group>
              </Col>
            </Row>
            <Row>
              <Button variant="outline-primary" type="submit" className="mt-3">
                Submit
              </Button>
            </Row>            
        </Col>
        <Col md = {4}>
            <ImageUpload setImageFile={setImageFile} />
        </Col>
        </Row>
    </Form>
  );
}

export default AddProductForm;