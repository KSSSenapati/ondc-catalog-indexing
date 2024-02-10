import data from '../data.json';
import Container from 'react-bootstrap/Container';
import Cards from '../components/cards';
import Row from 'react-bootstrap/Row';

const Home = () => {
    console.log(data)
    return(
        <Container fluid>
        <h2> All Products </h2>
        <Row>
            {data.product_list ? (
              data.product_list.map((product, key) => <Cards product={product} key={key} />)
            ) : (
              <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
                <h3>Error</h3>
              </div>
            )}
        </Row>
        </Container>
    )
}

export default Home;