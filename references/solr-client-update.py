import pysolr

# Create a connection to Solr
solr = pysolr.Solr('http://localhost:8983/solr/ondc', always_commit=True)

'''
generic format:-
create a dictionary 'doc' with all required fields (id, ad_enabled) and the field you want to update with the field value
create a dictionary 'updates' with all the fields that you want to update, with their appropriate modifier
'''

# update normal field
updates = {
    'discounted_price': 'set',
    'discount': 'set'
}

doc = {
    'id': 'doc_456',
    'discounted_price': 400,
    'discount': 20,
    'ad_enabled': False
}

# update multivalued field
updates = {
    'pincode': 'set'
}

doc = {
    'id': 'doc_456',
    'ad_enabled': False,
    'pincode': [761200, 761208]
}

# remove multivalued field
updates = {
    'pincode': 'remove'
}

doc = {
    'id': 'doc_456',
    'ad_enabled': False,
    'pincode': [761208]
}

# add multivalued field
updates = {
    'sizes_facet': 'add'
}

doc = {
    'id': 'doc_456',
    'ad_enabled': False,
    'sizes_facet': ['20g', '50g', '100g']
}

solr.add([doc], fieldUpdates=updates)
print("Partial update successful.")