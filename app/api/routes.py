from flask import Blueprint
from ..models import Product

api = Blueprint('api', __name__,url_prefix='/api')

@api.get('/api')
def apiCall():
    prod_data = Product.query.all()
    data_dic = [p.to_dict() for p in prod_data]
    for d in data_dic : 
        d['price'] = 9.99
    return {'status' : 'ok', 'data' : data_dic}