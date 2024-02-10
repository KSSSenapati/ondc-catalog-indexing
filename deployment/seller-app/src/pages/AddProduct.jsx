import Container from 'react-bootstrap/Container';

import AddProductForm from '../components/AddProductForm';
import Header from '../components/Header';

const AddProduct = () => {
    return(
        <>
            <Header />
            <Container>
                <AddProductForm />
            </Container>
        </>
    )
}

export default AddProduct;