import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';
import GlowCard from './GlowCard';

import ShowModal from './ShowModal';

import '../config';

function VerticallyCenteredModal(props) {
  const navigate = useNavigate();
    const [productId, setProductId] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        
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
                .then(response => response.json())
                .then(data => {
                  console.log(`raw: ${data.message}`)
                  navigate('/updateProduct', {state: {response: data.message}} )
                })
                .catch(err => console.log(err))
              break;
            case "Delete":
              fetch(global.config.url+"deleteProduct/"+productId, {method: 'delete'})
                .then(response => response.json())
                .then(data => {return(<ShowModal modalTitle="Delte Product" modalShow={true} modalContent={`Your Product ID ${productId} has been deleted.`}/>)})
                .catch(err => console.log(err))
              break;
            default:
              return 0;
          }
          
        }
    }

    return (
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
    );
}

function ProductModal({option}) {
  const [modalShow, setModalShow] = useState(false);

  const icons = {'Update': {_icon: 'fa fa-pencil', _description:"Helps in updating"}, 'Delete': {_icon: 'fa fa-trash', _description: 'helps in deleting Product'}}

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