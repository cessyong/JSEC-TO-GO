from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
from flask import flash
import database as db
import authentication
import logging
import pymongo
import ordermanagement as om

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)


@app.route('/')
def index():
    stall_list = db.get_stalls()
    return render_template('index.html', page="Index",stall_list=stall_list)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', page="Privacy")

# MAKE MANA
@app.route('/Mana')
def mana():
    mana_list = db.get_manaproducts()
    return render_template('mana.html', page="Mana",mana_list=mana_list)

# MAKE FAIRUZ
@app.route('/Fairuz')
def fairuz():
    fairuz_list = db.get_fairuzproducts()
    return render_template('fairuz.html', page="Fairuz",fairuz_list=fairuz_list)

# MAKE TAVERNA
@app.route('/Taverna')
def taverna():
    taverna_list = db.get_tavernaproducts()
    return render_template('taverna.html', page="Taverna",taverna_list=taverna_list)



# FAIRUZ
@app.route('/fairuzdetails')
def fairuzdetails():
    code = request.args.get('code', '')
    fairuz = db.get_fairuzproduct(int(code))
    return render_template('fairuzdetails.html', code=code,fairuz=fairuz)

# MANA
@app.route('/manadetails')
def manadetails():
    code = request.args.get('code', '')
    mana = db.get_manaproduct(int(code))
    return render_template('manadetails.html', code=code,mana=mana)

# TAVERNA
@app.route('/tavernadetails')
def tavernadetails():
    code = request.args.get('code', '')
    taverna = db.get_tavernaproduct(int(code))
    return render_template('tavernadetails.html', code=code,taverna=taverna)



@app.route('/stalls')
def stalls():
    stall_list = db.get_stalls()
    return render_template('stalls.html', page="Stalls",stall_list=stall_list)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")


@app.route('/myaccount')
def myaccount():
    return render_template('myaccount.html', page="My Account")


@app.route('/login' , methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    
    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        flash("Invalid username or password. Please try again.")
        return  render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')



@app.route('/addtocart', methods = ['POST', ])
def addtocart():
    code = request.form.get('code')
    quantity = int(request.form.get('quantity'))
    product = db.get_product(int(code))
    item=dict()
# A click to add a product translates to a quantity of 1 for now
    item["qty"] = quantity
    item["code"] = code
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]
    item["stall"] = product["stall"]
    
    
    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/foodtray')



@app.route('/foodtray')
def foodtray():
    return render_template('cart.html')


@app.route('/updatecart', methods = ['POST', ])
def updatecart():
    request_type = request.form.get('submit')
    code = request.form.get('code')
    product = db.get_product(int(code))
    cart = session["cart"]
    
    #Update quantity of item in cart
    if request_type == "Update":
        quantity = int(request.form.get("quantity"))
        cart[code]["qty"] = quantity
        cart[code]["subtotal"] = quantity * product["price"]
        
    elif request_type == 'Remove':
        del cart[code]
        
    session["cart"] = cart
    
    return redirect('/foodtray')


@app.route('/locations')
def locations():
    return render_template('locations.html', page="Locations")



@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')


@app.route('/orderhistory')
def orderhistory():
    user = session["user"]
    username = user["username"]
    
    arethereorders = om.check_user(username)
    
    if arethereorders == True:
        order_list = db.get_orders(username)
        return render_template('orderhistory.html', page="Orders", order_list=order_list)
    
    else:
        return render_template('orderempty.html')

    
@app.route('/changepassword')
def changepassword():
    return render_template('changepassword.html')

@app.route('/change', methods = ['GET', 'POST'])
def change():
    oldpass = request.form.get("old")
    newpass1 = request.form.get("new1")
    newpass2 = request.form.get("new2")
    user = session["user"]
    username = user["username"]
    userpass = user["password"]

    if oldpass == userpass and newpass1 == newpass2:
        change_now = db.change_db(username, newpass1)
        change_error = "Password successfully changed."
        return render_template('changepassword.html', change_error=change_error)
    
    elif oldpass != userpass:
        change_error = "The current password is incorrect."
        return render_template('changepassword.html', change_error=change_error)
    
    else:
        change_error = "The passwords entered do not match."
        return  render_template('changepassword.html', change_error=change_error)