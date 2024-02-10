import pysolr

# Create a connection to Solr
solr = pysolr.Solr('http://localhost:8983/solr/ondc', always_commit=True)

doc_id = 'doc_123'

# set id as the document's unique key
solr.delete(id=doc_id)
print("document deleted successfully")