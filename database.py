import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

stalls_db = myclient["stalls"]

menus_db = myclient["menus"]

products_db = myclient["products"]

order_management_db = myclient["order_management"]


# PRODUCTS
def get_product(code):
    products_coll = products_db["products"]
    
    product = products_coll.find_one({"code":code})
    
    return product

def get_products():
    product_list = []
    
    products_coll = products_db["products"]
    
    for p in products_coll.find({}):
        product_list.append(p)
        
    return product_list


# FAIRUZ
def get_fairuzproduct(code):
    fairuz_menu_coll = menus_db["fairuz_menu"]
    
    fairuz = fairuz_menu_coll.find_one({"code":code})
    
    return fairuz

def get_fairuzproducts():
    fairuz_list = []
    
    fairuz_menu_coll = menus_db["fairuz_menu"]
    
    for f in fairuz_menu_coll.find({}):
        fairuz_list.append(f)
        
    return fairuz_list

# MANA
def get_manaproduct(code):
    mana_menu_coll = menus_db["mana_menu"]
    
    mana = mana_menu_coll.find_one({"code":code})
    
    return mana

def get_manaproducts():
    mana_list = []
    
    mana_menu_coll = menus_db["mana_menu"]
    
    for m in mana_menu_coll.find({}):
        mana_list.append(m)
        
    return mana_list

# TAVERNA
def get_tavernaproduct(code):
    taverna_menu_coll = menus_db["taverna_menu"]
    
    taverna = taverna_menu_coll.find_one({"code":code})
    
    return taverna

def get_tavernaproducts():
    taverna_list = []
    
    taverna_menu_coll = menus_db["taverna_menu"]
    
    for t in taverna_menu_coll.find({}):
        taverna_list.append(t)
        
    return taverna_list



# NOT SURE IF WE NEED THIS PA
def get_stall(id):
    stalls_coll = stalls_db["stalls"]
    
    stall = stalls_coll.find_one({"stallid":stallid})
    
    return stall

def get_stalls():
    stall_list = []
    
    stalls_coll = stalls_db["stalls"]
    
    for s in stalls_coll.find({}):
        stall_list.append(s)
        
    return stall_list


def get_user(username):
    customers_coll = order_management_db['customers']
    user = customers_coll.find_one({"username":username})
    return user


def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)
    
def countorders(username):
    orders_coll = order_management_db['orders']
    numberoforders = orders_coll.count({"username":username})
    return numberoforders

def get_order(code):
    orders_coll = order_management_db['orders']
    
    order = orders_coll.find_one({"code":code})
    
    return order
    
def get_orders(username):
    order_list = []
    
    orders_coll = order_management_db['orders']
    
    for o in orders_coll.find({"username":username}):
        order_list.append(o)
        
    return order_list

def change_db(username, new1):
    pw_coll = order_management_db['customers']
    customer = {"username":username}
    changepw = {"$set": {"password":new1}}
    pw_coll.find_one_and_update(customer, changepw)