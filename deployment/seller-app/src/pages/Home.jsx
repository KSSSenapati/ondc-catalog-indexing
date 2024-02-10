import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col'
import { Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import ProductModal from '../components/ProductModal';
import Header from '../components/Header';

const Home = () => {
    return(
        <>
            <Header />
            <Container>
            <h2> Function </h2>
            <Row>
                <Col>
                    <Link to="/addProduct">
                        <Button variant="outline-primary">Add Product</Button>
                    </Link>
                </Col>
                <Col><ProductModal option="Update" /></Col>
                <Col><ProductModal option="Delete" /></Col>
            </Row>
            </Container>
        </>
    )
}

export default Home;