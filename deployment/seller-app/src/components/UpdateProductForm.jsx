import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Col } from 'react-bootstrap';
import { Row }from 'react-bootstrap';
import { ImageUpload } from './ImageUpload';
import { useEffect, useState } from 'react';
import Table from "react-bootstrap/Table";
import { TagsInput } from 'react-tag-input-component';

import data from '../data.json';
import ShowModal from './ShowModal';

const response = {
    "productTitle": "Delight Shirt", 
    "masterCategory": "apparel",
    "subCategory": "topwear",
    "article": "tshirts",
    "attribute": [{"fabric": "nylon"}, {"neck": "collar"}, {"fabric 2": "helllo"}],
    "price": "100",
    "discount": "10",
    "discountedPrice": "90",
    "acceleratorTags": ['hi', 'fwe'],
    "pinCode": ['129001309', '219831983', '31u13u']
}

function UpdateProductForm() {
  const [productTitle, setProductTitle] = useState(response['productTitle'])

  const masterCategoryList = Object.keys(data);
  const [subCategoryList, setSubCategoryList] = useState(Object.keys(data[response['masterCategory']]))
  const [articleList, setArticleList] = useState(Object.keys(data[response['masterCategory']][response['subCategory']]))

  const [masterCategory, setMasterCategory] = useState(response['masterCategory'])
  const [subCategory, setSubCategory] = useState(response['subCategory'])
  const [article, setArticle] = useState(response['article'])

  const [attribute, setAttribute] = useState(data[response['masterCategory']][response['subCategory']][response['article']])
  const [attributeValue, setAttributeValue] = useState([])

  const [imageFile, setImageFile] = useState()

  const [price, setPrice] = useState(response['price'])
  const [discount, setDiscount] = useState(response['discount'])
  const [discountedPrice, setDiscountedPrice] = useState(response['discountedPrice'])

  const [acceleratorTag, setAcceleratorTag] = useState(response['acceleratorTags'])
  const [pinCode, setPinCode] = useState(response['pinCode'])

  const [submitStatus, setSubmitStatus] = useState(false)

  const handleAttributeChange = (index, value) => {
    const updateValue = [...attributeValue];
    updateValue[index] = value;
    setAttributeValue(updateValue);
  }

  const getAttributeValue = () => {
    const new_ = new Array(attribute.length)

    response['attribute'].forEach((item) => {
        const _item = Object.keys(item)[0];
        new_[Array.from(attribute).indexOf(_item)] = item[_item];
    })

    setAttributeValue(new_)
  }

  useEffect(() => {getAttributeValue();}, [])

  const getAttributes = () => {
    const finalList = []
    attribute.forEach((item, index) => {
      if (attributeValue[index] !==  undefined) {
        const _attribute = {};
        _attribute[item] = attributeValue[index];
        finalList.push(_attribute);
      }
    })
    return finalList;
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const _payload = {
      "productTitle": productTitle,
      "masterCategory": masterCategory,
      "subCategory": subCategory,
      "article": article,
      "attribute": getAttributes(),
      "price": price,
      "discount": discount,
      "discountedPrice": discountedPrice,
      "acceleratorTags": acceleratorTag,
      "pinCode": pinCode,
      "image" : imageFile
    }
    setSubmitStatus(true);
    console.log(_payload);
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
    <Form onSubmit={(e) => handleSubmit(e)} className="pb-6">
      {submitStatus && <ShowModal modalBody="Your product id is" onClose={()=> setSubmitStatus(false)} modalShow={submitStatus} />}
        <Row>
        <h3 className='mb-3'>Update Product Form</h3>
        <Col md = {8}>
            <Row>
                <Form.Group className="mb-3" controlId="formProductTitle">
                    <Form.Label>Product Title</Form.Label>
                    <Form.Control required value={productTitle} type="text" placeholder="Enter Title" onChange={e => setProductTitle(e.target.value)}/>
                </Form.Group>
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
                    <Form.Select required value={subCategory} disabled={subCategoryList.length===0} onChange={(e) => {
                        setSubCategory(e.target.value);
                        e.target.value === "" ? handleEmpty(1) : setArticleList(Object.keys(data[masterCategory][e.target.value]));
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
                    <Form.Control required value={price} type="number" min="0" placeholder="Enter Price" onChange={(e) => {
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
                    <Form.Control type="number" value={discount} disabled={price==="0"} min="0" max="100" value={discount} placeholder="Enter Discount(%)" onChange={(e) => {
                      setDiscount(e.target.value);
                      setDiscountedPrice((1-(0.01 * e.target.value))* price);
                      }
                    }/>
                </Form.Group>
              </Col>
              <Col>
                <Form.Group className="mb-3" controlId="formDiscountedPrice">
                    <Form.Label>Discounted Price (INR) </Form.Label>
                    <Form.Control type="number" value={discountedPrice} disabled={price==="0"} min="0" max={price} value={discountedPrice} placeholder="Enter Discounted Price (INR)" onChange={(e) => {
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

export default UpdateProductForm;