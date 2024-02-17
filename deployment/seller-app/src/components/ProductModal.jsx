import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';
import GlowCard from './GlowCard';

import ShowModal from './ShowModal';

import '../config';
import Loader from './Loader';

function VerticallyCenteredModal(props) {
  const navigate = useNavigate();
    const [productId, setProductId] = useState("");
    const [childModalShow, setChildModalShow] = useState(false);
    const [loader, setLoader] = useState(false)

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoader(true);
        props.onHide();
        
        if(productId !== ""){
          props.onHide();
          switch(props.option){
            case "Update":
              const _options = {
                method: 'post',
                headers: {
                  "access-control-allow-origin" : "*",
                  "Content-Type": "application/json"
                },
                body: JSON.stringify({"product_id": productId})
              }
              fetch(global.config.url+"queryProduct", _options)
                .then((response) => {
                  setLoader(false);
                  return response.json();
                })
                .then(data => {
                  try {
                    console.log(`raw: ${data.status}`)
                    if(data.status === 'success') navigate('/updateProduct', {state: {response: data.message}} )
                  } catch(error) {console.log(error)}
                })
                .catch(err => console.log(err))
              break;
            case "Delete":
              fetch(global.config.url+"deleteProduct/"+productId, {method: 'delete'})
                .then((response) => {
                  setLoader(false);
                  return response.json()
                })
                .then(data => setChildModalShow(true))
                .catch(err => console.log(err))
              break;
            default:
              return 0;
          }
          
        }
    }

    return (
      <>
        {loader && <Loader />}
        <ShowModal modalTitle={`${props.option} Product`} modalShow={childModalShow} onClose={()=>setChildModalShow(false)} modalContent={`Your Product ID ${productId} has been ${props.option}d.`}/>
        <Modal
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
        >
            <Form>
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                Enter Product Id to {props.option}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form.Control reqired  type="text" placeholder="Product Id" onChange={(e) => setProductId(e.target.value)}/>
            </Modal.Body>
            <Modal.Footer>
                <Button type='submit' variant='outline-primary' onClick={handleSubmit}>Submit</Button>
            </Modal.Footer>
            </Form>
        </Modal>
        </>
    );
}

function ProductModal({option}) {
  const [modalShow, setModalShow] = useState(false);

  const icons = {'Update': {_icon: 'fa fa-pencil', _description:"You can update details about your product here."}, 'Delete': {_icon: 'fa fa-trash', _description: 'You can remove a product from your catalog here.'}}

  return (
    <>
      <GlowCard title={`${option} Product`} icon={icons[option]._icon} description={icons[option]._description} buttonFunction={()=>setModalShow(true)} />

      <VerticallyCenteredModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        option={option}
      />
    </>
  );
}

export default ProductModal;