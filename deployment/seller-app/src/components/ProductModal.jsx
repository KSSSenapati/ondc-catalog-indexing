import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';

function VerticallyCenteredModal(props) {
  const navigate = useNavigate();
    const [productId, setProductId] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if(productId !== ""){
          switch(props.option){
            case "Update":
              console.log("update");
              navigate('/updateProduct');
              break;
            case "Delete":
              console.log("delete");
              break;
            default:
              return 0;
          }
          props.onHide();
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

  return (
    <>
      <Button variant="outline-primary" onClick={() => setModalShow(true)}>
        {option} Product
      </Button>

      <VerticallyCenteredModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        option={option}
      />
    </>
  );
}

export default ProductModal;