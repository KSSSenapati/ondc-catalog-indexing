import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useState } from 'react';

function MyVerticallyCenteredModal(props) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Body closeButton>
        <p>
          {props.modalBody}
        </p>
      </Modal.Body>
    </Modal>
  );
}

function ShowModal({modalBody, modalShow, onClose}) {

  return (
    <>
      <MyVerticallyCenteredModal
        show={modalShow}
        onHide={() => {
            onClose()
        }}
        modalBody={modalBody}
      />
    </>
  );
}

export default ShowModal;