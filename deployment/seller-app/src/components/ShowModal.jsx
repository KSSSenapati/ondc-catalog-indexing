import Modal from 'react-bootstrap/Modal';

function MyVerticallyCenteredModal(props) {
  return (
    <Modal
      {...props}
      size="md"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <h4>{props.modalTitle}</h4>
      </Modal.Header>
      <Modal.Body>
        <p>
          {props.modalContent}
        </p>
      </Modal.Body>
    </Modal>
  );
}

function ShowModal({modalContent, modalShow, onClose, modalTitle}) {

  return (
    <>
      <MyVerticallyCenteredModal
        show={modalShow}
        onHide={() => {
            onClose()
        }}
        modalContent={modalContent}
        modalTitle={modalTitle}
      />
    </>
  );
}

export default ShowModal;