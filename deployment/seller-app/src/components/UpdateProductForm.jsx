import Button from 'react-bootstrap/Button';
import { useLocation } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import { Col } from 'react-bootstrap';
import { Row }from 'react-bootstrap';
import { ImageUpload } from './ImageUpload';
import { useEffect, useState } from 'react';
import Table from "react-bootstrap/Table";
import { TagsInput } from 'react-tag-input-component';

import data from '../data.json';
import ShowModal from './ShowModal';

import '../config';
import Loader from './Loader';

// const response = {
//     "product_id": "1323re2",
//     "product_title": "Delight Shirt",
//     "product_type": "Live",
//     "master_category": "apparel",
//     "sub_category": "topwear",
//     "article_type": "tshirts",
//     "attributes": {"fabric": "nylon", "neck": "collar", "fabric 2": "helllo"}, 
//     "price": "100",
//     "discount": "10",
//     "discounted_price": "90",
//     "accelerator_tag": ['hi', 'fwe'],
//     "pincode": ['129001309', '219831983', '31u13u']
// }

const UpdateProductForm = () => {
  const location = useLocation();
  const [loader, setLoader] = useState(false);

  const response = location.state.response;
  const [productTitle, setProductTitle] = useState(response['product_title'])

  const [productType, setProductType] = useState(response['product_type'])

  const masterCategoryList = Object.keys(data);
  const [subCategoryList, setSubCategoryList] = useState(Object.keys(data[response['master_category']]))
  const [articleList, setArticleList] = useState(Object.keys(data[response['master_category']][response['sub_category']]))

  const [masterCategory, setMasterCategory] = useState(response['master_category'])
  const [subCategory, setSubCategory] = useState(response['sub_category'])
  const [article, setArticle] = useState(response['article_type'])

  const [attribute, setAttribute] = useState(data[response['master_category']][response['sub_category']][response['article_type']])
  const [attributeValue, setAttributeValue] = useState([])

  const [imageFile, setImageFile] = useState()

  const [price, setPrice] = useState(response['price'])
  const [discount, setDiscount] = useState(response['discount'])
  const [discountedPrice, setDiscountedPrice] = useState(response['discounted_price'])

  const [acceleratorTag, setAcceleratorTag] = useState(response['accelerator_tag'] || [])
  const [pinCode, setPinCode] = useState(response['pincode'] || [])

  const [submitStatus, setSubmitStatus] = useState(false)

  const handleAttributeChange = (index, value) => {
    const updateValue = [...attributeValue];
    updateValue[index] = value;
    setAttributeValue(updateValue);
  }

  useEffect(() => {
    const new_ = new Array(attribute.length)
    attribute.forEach((item, index) => {
      if (Object.keys(response['attributes']).includes(item)) new_[index] = response['attributes'][item]
    });
    setAttributeValue(new_);
  }, [attribute, response])

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
    setLoader(true);
    const _payload = {
      "product_id": response['product_id'],
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

    const options = {
      method: 'post',
      headers: {
        "access-control-allow-origin" : "*",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(_payload)
    }

    fetch(global.config.url+"updateProduct", options)
        .then((response) => {
          setLoader(false);
          return response.json();
        })
        .then(response => setSubmitStatus(true))
        .catch(err => console.log(err)) 
  }

  const handleEmpty = (option) => {
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
      default:
        return 0;
    }
  }

  return (
    <>
    {loader && <Loader /> }
    <Form onSubmit={(e) => handleSubmit(e)} className="pb-6">
      {submitStatus && <ShowModal modalTitle="Update Successful" modalContent={`Your product id ${response['product_id']} has been updated.`} onClose={()=> setSubmitStatus(false)} modalShow={submitStatus} />}
        <Row>
        <h3 className='mb-3'>Update Product Form</h3>
        <Col md = {8}>
            <Row>
                <Col md={8}>
                <Form.Group className="mb-3" controlId="formProductTitle">
                    <Form.Label>Product Title</Form.Label>
                    <Form.Control required type="text" value={productTitle} placeholder="Enter Title" onChange={e => setProductTitle(e.target.value)}/>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="mb-3" controld="formMasterCategory" >
                    <Form.Label>Set Product Type</Form.Label>
                    <Form.Select required value={productType} onChange={(e) => setProductType(e.target.value)}>
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
                    <Form.Select required value={masterCategory} disabled={productTitle===""} onChange={(e) => {
                        setMasterCategory(e.target.value);
                        e.target.value === "" ? handleEmpty(2) : setSubCategoryList(Object.keys(data[e.target.value]));
                      }
                    }>
                      <option></option>
                      {masterCategoryList?.map((item, index)=> {
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
                    <Form.Select required value={subCategory} disabled={subCategoryList.length===0} onChange={(e) => {
                        setSubCategory(e.target.value);
                        e.target.value === "" ? handleEmpty(1) : setArticleList(Object.keys(data[masterCategory][e.target.value]));
                      }
                    }>
                      <option></option>
                      {subCategoryList.length!== 0 && subCategoryList?.map((item, index)=> {
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
                    <Form.Select required value={article} disabled={articleList.length===0} onChange={(e) => {
                      setArticle(e.target.value);
                      if (e.target.value !== "") {
                        const list_ = data[masterCategory][subCategory][e.target.value]
                        setAttribute(list_);
                        setAttributeValue(new Array(list_.length))
                      } else {
                        handleEmpty(0)
                      }
                    }
                    }>
                      <option></option>
                      {articleList.length!== 0 && articleList?.map((item, index)=> {
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
                    {attribute?.map((item, index) => {
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
                    <Form.Control required value={price} type="number" min="0" placeholder="Enter Price" onChange={(e) => {
                      const val_ = e.target.value;
                      setPrice(val_);
                      if (discount !== 0) setDiscountedPrice(((1-(0.01 * discount))* val_).toFixed(2));
                      }
                    }/>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="mb-3" controlId="formDiscount">
                    <Form.Label>Discount (%) </Form.Label>
                    <Form.Control type="number" value={discount} disabled={price==="0"} step="0.01" min="0" max="100" placeholder="Enter Discount(%)" onChange={(e) => {
                      setDiscount(e.target.value);
                      setDiscountedPrice(((1-(0.01 * e.target.value))* price).toFixed(2));
                      }
                    }/>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="mb-3" controlId="formDiscountedPrice">
                    <Form.Label>Discounted Price (INR) </Form.Label>
                    <Form.Control type="number" value={discountedPrice} disabled={price==="0"} step="0.01" min="0" placeholder="Enter Discounted Price (INR)" onChange={(e) => {
                      setDiscountedPrice(e.target.value);
                      setDiscount(((1 - e.target.value/price) * 100).toFixed(2));
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
  </>
  );
}

export default UpdateProductForm;