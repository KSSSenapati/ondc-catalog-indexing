import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import EditProduct from './editProduct';
import styles from '../style/cards.module.scss';

const Cards = ({product}) => {
  return (
    <Col xs={6} sm = {4} md= {2}>
        <Card className={styles.card}>
        <Card.Img variant="top" src={product.image} className={styles.img} />
        <Card.Body>
            <Card.Title>{product.title}</Card.Title>
            <Card.Text>
            {product.price}
            </Card.Text>
            
        </Card.Body>
        <Card.Footer>
            <EditProduct data={product}/>
        </Card.Footer>
        </Card>
    </Col>
  );
}

export default Cards;