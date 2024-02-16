import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col'
import { useNavigate } from 'react-router-dom';
import GlowCard from '../components/GlowCard';

import ProductModal from '../components/ProductModal';
import Header from '../components/Header';
import '../style/home2.css'

const Home = () => {
    const navigate = useNavigate();
    const handleSubmit = (e) => {
        e.preventDefault()
        navigate('/addProduct');
    }
    return(
        <>
            <Header />
            <Container>
                <Row className='glow-container'>
                    <Col><GlowCard title='Add Product' icon='fa fa-plus-circle' description='You can onboard a new product your catalog from here.' buttonFunction={(e) => handleSubmit(e)} /></Col>
                    <Col><ProductModal option="Update" /></Col>
                    <Col><ProductModal option="Delete" /></Col>
                </Row>
            </Container>
        </>
    )
}

export default Home;