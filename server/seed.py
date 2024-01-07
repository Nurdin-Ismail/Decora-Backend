from app import  app
from models import *
import json
from faker import Faker
import random
import os




with app.app_context():
    fake = Faker()
    
    Product.query.delete()
    Image.query.delete()
    User.query.delete()
    
    text_file = open('/home/nurdin/Projects/Decora_Backend/json', 'r')

    text_file1 = text_file.read()
    # print(text_file1)
    data = json.loads(text_file1)
    filtered = []
    
    target_names = []
    
    for i in data:
        target_names.append(i['PRODUCT NAME'])
        
    
        
 
    
   
    #directory for all the product images
    my_dir = '/home/nurdin/Projects/exercise/Productimages'
    #list for names of the directories that contain the images
    names = []
    for dir, sub, fileso in os.walk(my_dir):
    
        if dir != '/home/nurdin/Projects/exercise/Productimages':
            if sub:
                names.append(sub)
                # print(sub)
                # print(fileso)
        

    resultList = []

# Traversing in till the length of the input list of lists
# 
    for m in range(len(names)):

   # using nested for loop, traversing the inner lists
        for n in range (len(names[m])):

      # Add each element to the result list
            resultList.append(names[m][n])
            
            
    common_names = [name for name in resultList if name in target_names]
    
    # print("Common names:")
    
    # print(common_names)
    
    for i in data:
        if i.get("RECEIVED QUANTITY") and i.get('DESCRIPTION'):
            filtered.append(i)
            
    name_counts = {}
    for item in data:
        name = item.get('PRODUCT NAME')
        name_counts[name] = name_counts.get(name, 0) + 1

# Filter dictionaries with unique 'name' key
    # filtered_data = [item for item in filtered if name_counts[item['PRODUCT NAME']] == 1 and name_counts[item['PRODUCT NAME']] in common_names]
    filtered_data = []
    
    for item in range(len(filtered)):
        if filtered[item]['PRODUCT NAME'] in common_names and name_counts[filtered[item]['PRODUCT NAME']] == 1:
            filtered_data.append(filtered[item])
    
    
    # item = filtered[230]['PRODUCT NAME']
    # if item in common_names:
    #     print('Item: ', item)
        
    # for item in range(len(filtered)):
    #     if filtered[item]['PRODUCT NAME'] in common_names:
    #         print('Item: ', filtered[item]['PRODUCT NAME'])
            
    filtered_common_names = []   
    for item in filtered_data:
        if item['PRODUCT NAME'] in common_names:
            filtered_common_names.append(item["PRODUCT NAME"])
    print('filtered names' ,len(filtered_common_names))
    # print(filtered_data)
    
    print(len(filtered_data))
        
     #POPULATING PRODUCTS TABLE       
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
    
    
    # print(Product.query.all())
    
    #POPULATING IMAGES TABLE
    for path, sub, fileso in os.walk(my_dir):
        for item in filtered_common_names:
            if item in path:
                # print(item ,fileso)
                
                product = Product.query.filter(Product.name == item).first()
                
                
                images = []
                fileso.sort()
                for img in fileso:
                      image = open(path + '/' + img, 'rb')
                      
                      imeji = Image(
                          product_id = product.id,
                          img = image.read(),
                          name = img,
                          mimetype = 'image/jpg'
                          
                      )
                      
                      images.append(imeji)
                db.session.add_all(images)
                db.session.commit()
                
    print("Imagess successfully populated") 
    
    #POPULATING USERS TABLE
    list_of_usernames = []
    for _ in range(100):
        list_of_usernames.append(fake.name())
        
    users = []
    for user in list_of_usernames:
        new_user = User(
            username = user,
            # location = fake.address(),
            email = fake.email(),
            password = fake.password(),
            contacts = fake.phone_number(),
            
            
        )
        users.append(new_user)
    db.session.add_all(users)
    db.session.commit()
    print("Users successfully populated")
    
    
    #POPULATING CARTS
    
    carts= []
    for i in range(50):
        user = random.randrange(1,101)
        product = random.randrange(1,78)
        cart = Cart(
            user_id = user,
            product_id = product
        )
        
        carts.append(cart)
    
        
    db.session.add_all(carts)
    db.session.commit()
    print("Carts successfully populated")   
        
    
    
                          
                      
                      
                      
                      
                
        

    # resultList = []
    
    






if __name__ == '__main__':
    app.run(port=5555)