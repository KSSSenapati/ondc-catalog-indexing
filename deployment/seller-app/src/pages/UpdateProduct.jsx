import Container from 'react-bootstrap/Container';
import Header from '../components/Header';
import UpdateProductForm from '../components/UpdateProductForm';

const UpdateProduct = () => {
    return(
        <>
            <Header />
            <Container>
                <UpdateProductForm />
            </Container>
        </>
    )
}

export default UpdateProduct;