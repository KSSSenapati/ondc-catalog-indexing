import pysolr

# Create a connection to Solr
solr = pysolr.Solr('http://localhost:8983/solr/ondc', always_commit=True)

# Define your document data
doc = {
    'id': 'doc_' + str(456),  # Example of mixing string and int
    'product_id': 456,  # Example of integer
    'product_title': 'This is a Product Title',  # Example of string
    'price': 500,  # Example of float
    'discounted_price': 357,  # Example of float
    'discount': 28.6
    # Add more fields as needed
}

# Add or update the document in Solr
solr.add([doc])
print("document added")
