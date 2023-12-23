from app import  app
from models import *
import json


with app.app_context():
    
    Product.query.delete()
    
    text_file = open('/home/nurdin/Projects/Decora_Backend/json', 'r')

    text_file1 = text_file.read()
    data = json.loads(text_file1)
    filtered = []
    for i in data:
        if i.get("RECEIVED QUANTITY") and i.get('DESCRIPTION'):
            filtered.append(i)
            
    name_counts = {}
    for item in data:
        name = item.get('PRODUCT NAME')
        name_counts[name] = name_counts.get(name, 0) + 1

# Filter dictionaries with unique 'name' key
    filtered_data = [item for item in filtered if name_counts[item['PRODUCT NAME']] == 1]
        
            
    products = []
    for product in filtered_data:
        new_product = Product(
        name=product['PRODUCT NAME'],
        description = product['DESCRIPTION'],
        category = product["CATEGORY"],
        sub_category = product["SUB-CATEGORY"],
        tag = product["PRODUCT TYPE"],
        price = product['SELLING PRICE'],
        quantity = product["RECEIVED QUANTITY"]
                     
    )
        products.append(new_product)
    db.session.add_all(products)
    db.session.commit()
    
    print("Products successfully populated")
    print(data[9]["RECEIVED QUANTITY"])
    
    # print(data[0]['PRODUCT NAME'])
    
    






if __name__ == '__main__':
    app.run(port=5555)