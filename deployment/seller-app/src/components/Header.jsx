import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { useNavigate } from 'react-router-dom';

function Header() {
  const navigate = useNavigate();
  return (
    <Navbar expand="lg" className="bg-body-tertiary " style={{cursor: 'pointer', marginBottom: "5rem"}}>
      <Container >
        <Navbar.Brand onClick={() => navigate('/')}><img src={`${process.env.PUBLIC_URL}/assets/cyborg_logo_black.png`} alt="logo" height={50} style={{marginRight: "30px"}}/>Seller Application</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll">
          <Nav
            className="ms-auto"
            style={{ maxHeight: '100px' }}
            navbarScroll
          >
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="#footer">Contact Us</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;