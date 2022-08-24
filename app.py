from flask import Flask, render_template, render_template_string, request,redirect,url_for,session
import psycopg2
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import date

today = date.today()

app = Flask(__name__)
app.secret_key="hello"

conn = psycopg2.connect(
   database="d67fsm4svq5gp3", user='cthlqzrfduldux', password='284d42f2d7277cf2318c7053bb11f6665c3ba385f1abc9ca3668af049a5eb06e', host='ec2-44-195-100-240.compute-1.amazonaws.com', port= '5432'
)
c = conn.cursor()


@app.route('/', methods=["GET","POST"])
def index():
    conn.rollback()
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        c.execute("SELECT username FROM users;")
        usernames = (c.fetchall())
        usernames_list=[]

        for i in usernames:
            usernames_list.append(i[0])
        conn.commit()
        
        c.execute("SELECT password FROM users;")
        passwords = (c.fetchall())
        passwords_list=[]

        for i in passwords:
            passwords_list.append(i[0])
        conn.commit()

        if username in usernames_list:
            if password in passwords_list:
                session.permanent=False
                session["user"]=username
                c.execute("""SELECT user_type FROM users WHERE username = %(value)s; """,{"value":username})
                user_type = (c.fetchall())
                if user_type[0][0]=="admin":
                    return redirect (url_for("admin"))
                elif user_type[0][0]=="sales":
                    return redirect (url_for("sales"))

    return render_template("index.html")


@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")

@app.route("/sales", methods=["GET"])
def sales():
    return render_template("sales.html")



@app.route('/new_user', methods=["GET","POST"])
def new_user():

   if "user" in session:

    c.execute("""SELECT * FROM users""")
    users_select = c.fetchall()
    conn.commit()
    user_list = []
    for i in range(len(users_select)):
        each_user=[users_select[i][0],users_select[i][1],users_select[i][2]]
        user_list.append(each_user)


    if request.method=="POST":
        if request.form.get("delete")=="delete":
            username_to_delete=request.form.get("username_table")
            c.execute("""DELETE FROM users WHERE username='{value1}'""".format(value1=username_to_delete))
            conn.commit()
            return redirect(url_for("new_user", users=user_list, name=username_to_delete))

        if request.form.get("create")=="create":
            username = request.form.get("username")
            password = request.form.get("password")
            user_type = request.form.get("user_type")
            c.execute("""INSERT INTO users(username,password,user_type) VALUES('{value1}','{value2}','{value3}')""".format(value1=username,value2=password,value3=user_type))
            conn.commit()
        
        if request.form.get("edit")=="edit":
            session['username_to_edit'] = request.form.get("username_table")
            return redirect(url_for("user_edit"))


    return render_template("new_user.html", users=user_list)
   return render_template("index.html")
    
@app.route('/user_edit', methods=["GET","POST"])
def user_edit():
    
    username_to_edit=session['username_to_edit']

    c.execute("""SELECT * FROM users""")
    users_select = c.fetchall()
    conn.commit()
    user_list = []
    for i in range(len(users_select)):
        each_user=[users_select[i][0],users_select[i][1],users_select[i][2]]
        user_list.append(each_user)

    if request.method=="POST":
        username = request.form.get("username_edit")
        password = request.form.get("password_edit")
        user_type = request.form.get("user_type_edit")
        c.execute("""UPDATE users SET username='{value1}',password='{value2}',user_type='{value3}' WHERE username='{value4}'""".format(value1=username,value2=password,value3=user_type, value4=username_to_edit))
        conn.commit()
        session.pop('username_to_edit')

        return redirect(url_for("new_user", users=user_list))
    return render_template("user_edit.html")

@app.route('/new_product', methods=["GET","POST"])
def new_product():

   if "user" in session:

    c.execute("""SELECT * FROM products""")
    product_select = c.fetchall()
    conn.commit()
    product_list = []
    for i in range(len(product_select)):
        each_product=[product_select[i][0],product_select[i][1],product_select[i][2],product_select[i][3],product_select[i][4],product_select[i][5],product_select[i][6],product_select[i][7]]
        product_list.append(each_product)


    if request.method=="POST":
        if request.form.get("delete")=="delete":
            product_id_to_delete=request.form.get("product_id_table")
            c.execute("""DELETE FROM products WHERE product_name='{value1}'""".format(value1=product_id_to_delete))
            conn.commit()
            return redirect(url_for("new_product", product=product_list))

        if request.form.get("create")=="create":
            product_id = request.form.get("product_id")
            product_name = request.form.get("product_name")
            product_height = request.form.get("product_height")
            product_width = request.form.get("product_width")
            product_weight = request.form.get("product_weight")
            product_cost = request.form.get("product_cost")
            product_mrp = request.form.get("product_mrp")
            product_description = request.form.get("product_description")

            c.execute("""INSERT INTO products(product_id,product_name,product_height,product_width,product_weight,product_cost,product_mrp,product_description) VALUES('{value1}','{value2}','{value3}','{value4}','{value5}','{value6}','{value7}','{value8}')""".format(value1=product_id,value2=product_name,value3=product_height,value4=product_width,value5=product_weight,value6=product_cost,value7=product_mrp,value8=product_description))
            conn.commit()
        
        if request.form.get("edit")=="edit":
            session['product_id_to_edit'] = request.form.get("product_id_table")
            return redirect(url_for("product_edit"))


    return render_template("new_product.html", product=product_list)
   return render_template("index.html")

@app.route('/product_edit', methods=["GET","POST"])
def product_edit():
    
    product_id_to_edit=session['product_id_to_edit']

    c.execute("""SELECT * FROM products""")
    product_select = c.fetchall()
    conn.commit()
    product_list = []
    for i in range(len(product_select)):
        each_product=[product_select[i][0],product_select[i][1],product_select[i][2],product_select[i][3],product_select[i][4],product_select[i][5],product_select[i][6],product_select[i][7]]
        product_list.append(each_product)

    if request.method=="POST":
        product_id = request.form.get("product_id_edit")
        product_name = request.form.get("product_name_edit")
        product_height = request.form.get("product_height_edit")
        product_width = request.form.get("product_width_edit")
        product_weight = request.form.get("product_weight_edit")
        product_cost = request.form.get("product_cost_edit")
        product_mrp = request.form.get("product_mrp_edit")
        product_description = request.form.get("product_description_edit")
        c.execute("""UPDATE users SET product_id='{value1}',product_name='{value2}',product_height='{value3},product_height='{value4},product_weight='{value5},product_cost='{value6},product_mrp='{value7},product_description='{value8}' WHERE product_id='{value9}'""".format(value1=product_id,value2=product_name,value3=product_height,value4=product_width,value5=product_weight,value6=product_cost,value7=product_mrp,value8=product_description,value9=product_id_to_edit ))
        conn.commit()
        session.pop('product_id_to_edit')

        return redirect(url_for("new_product", product=product_list))
    return render_template("product_edit.html")

@app.route('/customer_edit', methods=['GET','POST'])
def customer_edit():

    customer_id_to_edit=session['customer_id_to_edit']

    c.execute('SELECT * FROM customers')
    customers_select = c.fetchall()
    conn.commit()
    customers_list = []
    column =[]
    for i in range(len(customers_select)):
        for j in range(len(customers_select[i])):
            each_item=customers_select[i][j]
            column.append(each_item)
        customers_list.append(column)
    if request.method=="POST":
            customer_id=request.form.get('customer_id_edit')
            customer_name=request.form.get('customer_name_edit')
            customer_address=request.form.get('customer_address_edit')
            customer_type=request.form.get('customer_type_edit')
            customer_gst=request.form.get('customer_gst_edit')
            customer_contact=request.form.get('customer_contact_edit')
            c.execute("""UPDATE customers SET customer_id='{value1}',customer_name='{value2}',customer_address='{value3}',customer_type='{value4}',customer_gst='{value5}',customer_contact='{value6}' WHERE customer_id='{value9}'""".format(value1=customer_id,value2=customer_name,value3=customer_address,value4=customer_type,value5=customer_gst,value6=customer_contact,value9=customer_id_to_edit ))
            conn.commit()
            session.pop('customer_id_to_edit')
            return redirect(url_for("new_customer", data=customers_list))
    return render_template("customer_edit.html")



@app.route('/new_customer', methods=['GET','POST'])
def new_customer():
    
    
   if "user" in session:
        c.execute('SELECT * FROM customers')
        customers_select = c.fetchall()
        conn.commit()
        customers = []
        column =[]
        for i in range(len(customers_select)):
            for j in range(len(customers_select[i])):
                each_item=customers_select[i][j]
                column.append(each_item)
            customers.append(column)
    
        if request.method=="POST":
            if request.form.get("delete")=="delete":
                to_delete=request.form.get("customer_id_table")
                c.execute("DELETE FROM customers WHERE customer_id='{to_delete}'".format(to_delete=to_delete))
                conn.commit()
    
        if request.form.get("create")=="create":

            customer_id=request.form.get("customer_id")
            customer_name=request.form.get("customer_name")
            customer_address=request.form.get("customer_address")
            customer_type=request.form.get("customer_type")
            customer_gst=request.form.get("customer_gst")
            customer_contact=request.form.get("customer_contact")
            c.execute("""INSERT INTO customers(customer_id,customer_name,customer_address,customer_type,customer_gst,customer_contact) VALUES('{value1}','{value2}','{value3}','{value4}','{value5}','{value6}')""".format(value1=customer_id,value2=customer_name,value3=customer_address,value4=customer_type,value5=customer_gst,value6=customer_contact))
            conn.commit()

        if request.form.get("edit")=="edit":
            session['customer_id_to_edit'] = request.form.get("customer_id_table")
            return redirect(url_for("customer_edit"))
        return render_template("new_customer.html", data=customers)
   return render_template("index.html")



@app.route('/new_door_pattern', methods=['GET','POST'])
def new_door_pattern():
    
    
   if "user" in session:
        c.execute('SELECT * FROM door_pattern')
        door_pattern_select = c.fetchall()
        conn.commit()
        door_pattern = []
        column =[]
        for i in range(len(door_pattern_select)):
            for j in range(len(door_pattern_select[i])):
                each_item=door_pattern_select[i][j]
                column.append(each_item)
            door_pattern.append(column)
    
        if request.method=="POST":
            if request.form.get("delete")=="delete":
                to_delete=request.form.get("door_pattern_id_table")
                c.execute("DELETE FROM door_pattern WHERE door_pattern_id='{to_delete}'".format(to_delete=to_delete))
                conn.commit()
    
        if request.form.get("create")=="create":
 
                door_pattern_id=request.form.get('door_pattern_id')
                door_pattern=request.form.get('door_pattern')

                c.execute("INSERT INTO door_pattern(door_pattern_id,door_pattern) VALUES('{value1}','{value2}')".format(value1=door_pattern_id,value2=door_pattern))
                conn.commit()

        if request.form.get("edit")=="edit":
            session['door_pattern_id_to_edit'] = request.form.get("door_pattern_id_table")
            return redirect(url_for("door_pattern_edit"))
        return render_template("new_door_pattern.html", data=door_pattern)
   return render_template("index.html")



@app.route('/door_pattern_edit', methods=['GET','POST'])
def door_pattern_edit():

    door_pattern_id_to_edit=session['door_pattern_id_to_edit']

    c.execute('SELECT * FROM door_pattern')
    door_pattern_select = c.fetchall()
    conn.commit()
    door_pattern_list = []
    column =[]
    for i in range(len(door_pattern_select)):
        for j in range(len(door_pattern_select[i])):
            each_item=door_pattern_select[i][j]
            column.append(each_item)
        door_pattern_list.append(column)
    if request.method=="POST":
            door_pattern_id=request.form.get('door_pattern_id_edit')
            door_pattern=request.form.get('door_pattern_edit')
            c.execute("""UPDATE customers SET door_pattern_id='{value1}',door_pattern='{value2}' WHERE customer_id='{value9}'""".format(value1=door_pattern_id,value2=door_pattern,value9=door_pattern_id_to_edit ))
            conn.commit()
            session.pop('door_pattern_id_to_edit')
            return redirect(url_for("new_door_pattern", data=door_pattern_list))
    return render_template("door_pattern_edit.html")


@app.route('/new_profile', methods=['GET','POST'])
def new_profile():
    
    
   if "user" in session:
        c.execute('SELECT * FROM profile')
        profile_select = c.fetchall()
        conn.commit()
        profile = []
        column =[]
        for i in range(len(profile_select)):
            for j in range(len(profile_select[i])):
                each_item=profile_select[i][j]
                column.append(each_item)
            profile.append(column)
    
        if request.method=="POST":
            if request.form.get("delete")=="delete":
                to_delete=request.form.get("profile_id_table")
                c.execute("DELETE FROM profile WHERE profile_id='{to_delete}'".format(to_delete=to_delete))
                conn.commit()
    
        if request.form.get("create")=="create":
                profile_id=request.form.get('profile_id')
                profile=request.form.get('profile')

                c.execute("INSERT INTO profile(profile_id,profile) VALUES('{value1}','{value2}')".format(value1=profile_id,value2=profile))
                conn.commit()

        if request.form.get("edit")=="edit":
            session['profile_id_to_edit'] = request.form.get("profile_id_table")
            return redirect(url_for("profile_edit"))
        return render_template("new_profile.html", data=profile)
   return render_template("index.html")

@app.route('/profile_edit', methods=['GET','POST'])
def profile_edit():

    profile_id_to_edit=session['profile_id_to_edit']

    c.execute('SELECT * FROM profile')
    profile_select = c.fetchall()
    conn.commit()
    profile_list = []
    column =[]
    for i in range(len(profile_select)):
        for j in range(len(profile_select[i])):
            each_item=profile_select[i][j]
            column.append(each_item)
        profile_list.append(column)
    if request.method=="POST":
            profile_id=request.form.get('profile_id_edit')
            profile=request.form.get('profile_edit')
            c.execute("""UPDATE customers SET profile_id='{value1}',profile='{value2}' WHERE customer_id='{value9}'""".format(value1=profile_id,value2=profile,value9=profile_id_to_edit ))
            conn.commit()
            session.pop('profile_id_to_edit')
            return redirect(url_for("new_profile", data=profile_list))
    return render_template("profile_edit.html")

@app.route('/new_room', methods=['GET','POST'])
def new_room():
    
    
   if "user" in session:
        c.execute('SELECT * FROM room')
        room_select = c.fetchall()
        conn.commit()
        room = []
        column =[]
        for i in range(len(room_select)):
            for j in range(len(room_select[i])):
                each_item=room_select[i][j]
                column.append(each_item)
            room.append(column)
    
        if request.method=="POST":
            if request.form.get("delete")=="delete":
                to_delete=request.form.get("room_id_table")
                c.execute("DELETE FROM room WHERE room_id='{to_delete}'".format(to_delete=to_delete))
                conn.commit()
    
        if request.form.get("create")=="create":
                room_id=request.form.get('room_id')
                room=request.form.get('room')
                c.execute("INSERT INTO room(room_id,room) VALUES('{value1}','{value2}')".format(value1=room_id,value2=room))
                conn.commit()

        if request.form.get("edit")=="edit":
                    session['room_id_to_edit'] = request.form.get("room_id_table")
                    return redirect(url_for("room_edit"))
        return render_template("new_room.html", data=room)
   return render_template("index.html")


@app.route('/room_edit', methods=['GET','POST'])
def room_edit():

        room_id_to_edit=session['room_id_to_edit']

        c.execute('SELECT * FROM room')
        room_select = c.fetchall()
        conn.commit()
        room_list = []
        column =[]
        for i in range(len(room_select)):
            for j in range(len(room_select[i])):
                each_item=room_select[i][j]
                column.append(each_item)
            room_list.append(column)
        if request.method=="POST":
                room_id=request.form.get('room_id_edit')
                room=request.form.get('room_edit')
                c.execute("""UPDATE room SET room_id='{value1}',room='{value2}' WHERE customer_id='{value9}'""".format(value1=room_id,value2=room,value9=room_id_to_edit ))
                conn.commit()
                session.pop('room_id_to_edit')
                return redirect(url_for("new_room", data=room_list))
        return render_template("room_edit.html")


@app.route('/new_collection', methods=['GET','POST'])
def new_collection():
    
    
   if "user" in session:
        c.execute('SELECT * FROM collection')
        collection_select = c.fetchall()
        conn.commit()
        collection = []
        column =[]
        for i in range(len(collection_select)):
            for j in range(len(collection_select[i])):
                each_item=collection_select[i][j]
                column.append(each_item)
            collection.append(column)
    
        if request.method=="POST":
            if request.form.get("delete")=="delete":
                to_delete=request.form.get("collection_id_table")
                c.execute("DELETE FROM collection WHERE collection_id='{to_delete}'".format(to_delete=to_delete))
                conn.commit()
    
        if request.form.get("create")=="create":
                collection_id=request.form.get('collection_id')
                collection=request.form.get('collection')
                c.execute("INSERT INTO collection(collection_id,collection) VALUES('{value1}','{value2}')".format(value1=collection_id,value2=collection))
                conn.commit()

        if request.form.get("edit")=="edit":
            session['collection_id_to_edit'] = request.form.get("collection_id_table")
            return redirect(url_for("collection_edit"))
        return render_template("new_collection.html", data=collection)
   return render_template("index.html")

@app.route('/collection_edit', methods=['GET','POST'])
def collection_edit():

        collection_id_to_edit=session['collection_id_to_edit']

        c.execute('SELECT * FROM collection')
        collection_select = c.fetchall()
        conn.commit()
        collection_list = []
        column =[]
        for i in range(len(collection_select)):
            for j in range(len(collection_select[i])):
                each_item=collection_select[i][j]
                column.append(each_item)
            collection_list.append(column)
        if request.method=="POST":
                collection_id=request.form.get('collection_id_edit')
                collection=request.form.get('collection_edit')
                c.execute("""UPDATE collection SET collection_id='{value1}',collection='{value2}' WHERE customer_id='{value9}'""".format(value1=collection_id,value2=collection,value9=collection_id_to_edit ))
                conn.commit()
                session.pop('collection_id_to_edit')
                return redirect(url_for("new_collection", data=collection_list))
        return render_template("collection_edit.html")

@app.route('/new_highlight', methods=['GET','POST'])
def new_highlight():
    
    
   if "user" in session:
        c.execute('SELECT * FROM highlight')
        highlight_select = c.fetchall()
        conn.commit()
        highlight = []
        column =[]
        for i in range(len(highlight_select)):
            for j in range(len(highlight_select[i])):
                each_item=highlight_select[i][j]
                column.append(each_item)
            highlight.append(column)
    
        if request.method=="POST":
            if request.form.get("delete")=="delete":
                to_delete=request.form.get("highlight_id_table")
                c.execute("DELETE FROM highlight WHERE highlight_id='{to_delete}'".format(to_delete=to_delete))
                conn.commit()
    
        if request.form.get("create")=="create":
                highlight_id=request.form.get('highlight_id')
                highlight=request.form.get('highlight')
                c.execute("INSERT INTO highlight(highlight_id,highlight) VALUES('{value1}','{value2}')".format(value1=highlight_id,value2=highlight))
                conn.commit()

        if request.form.get("edit")=="edit":
            session['highlight_id_to_edit'] = request.form.get("highlight_id_table")
            return redirect(url_for("highlight_edit"))
        return render_template("new_highlight.html", data=highlight)
   return render_template("index.html")


@app.route('/highlight_edit', methods=['GET','POST'])
def highlight_edit():

            highlight_id_to_edit=session['highlight_id_to_edit']

            c.execute('SELECT * FROM highlight')
            highlight_select = c.fetchall()
            conn.commit()
            highlight_list = []
            column =[]
            for i in range(len(highlight_select)):
                for j in range(len(highlight_select[i])):
                    each_item=highlight_select[i][j]
                    column.append(each_item)
                highlight_list.append(column)
            if request.method=="POST":
                    highlight_id=request.form.get('highlight_id_edit')
                    highlight=request.form.get('highlight_edit')
                    c.execute("""UPDATE collection SET highlight_id='{value1}',highlight='{value2}' WHERE highlight_id='{value9}'""".format(value1=highlight_id,value2=highlight,value9=highlight_id_to_edit ))
                    conn.commit()
                    session.pop('highlight_id_to_edit')
                    return redirect(url_for("new_highlight", data=highlight_list))
            return render_template("highlight_edit.html")

@app.route('/new_opr_customer', methods=['GET','POST'])
def new_opr_customer():

            

            c.execute('SELECT customer_name FROM customers')
            customer_opr_select = c.fetchall()
            conn.commit()
            customer_opr_list = []
            column =[]
            for i in range(len(customer_opr_select)):
                for j in range(len(customer_opr_select[i])):
                    each_item=customer_opr_select[i][j]
                    column.append(each_item)
                customer_opr_list.append(each_item)

            # c.execute("""SELECT customer_contact WHERE customer_name='{value1}'""".format(value1=customer_opr_list))
            if request.method=="POST":

                    session['customer_opr'] = request.form.get("customer_opr")
                    session['delivery_address'] = request.form.get("delivery_address")
                    session['preferred_delivery_time'] = request.form.get("preferred_delivery_time")
                    session['cargo_vehicle_time'] = request.form.get("cargo_vehicle_time")
                    session['floor_number'] = request.form.get("floor_number")
                    session['lift_available'] = request.form.get("lift_available")
                    session['opr_id'] = request.form.get("opr_id")
                    session["flat_number"]=request.form.get("flat_number")
                    session["discount"]=request.form.get("discount")

                    c.execute("""INSERT INTO customer_opr(opr_id,customer_opr,delivery_address,preferred_delivery_time,cargo_vehicle_time,floor_number,lift_available,flat_number,discount)
                                VALUES('{value1}','{value2}','{value3}','{value4}','{value5}','{value6}','{value7}','{value8}','{value9}')""".format(value1=session["opr_id"],value2=session["customer_opr"],value3=session["delivery_address"],value4=session["preferred_delivery_time"],value5=session["cargo_vehicle_time"],value6=session["floor_number"],value7=session["lift_available"],value8=session["flat_number"],value9=session["discount"]))


                    return redirect(url_for("new_opr_generation", data=customer_opr_list))
            return render_template("new_opr_customer.html",data=customer_opr_list)

@app.route('/new_opr_generation', methods=['GET','POST'])
def new_opr_generation():
    
    customer_opr =session['customer_opr'] 
    delivery_address = session['delivery_address'] 
    preferred_delivery_time =session['preferred_delivery_time'] 
    cargo_vehicle_time =session['cargo_vehicle_time'] 
    floor_number  =session['floor_number'] 
    lift_available=session['lift_available']
    opr_id=session['opr_id']
    discount=session["discount"]
    
    session["date"]=date.today()

    c.execute('SELECT product_name FROM products')
    product_select = c.fetchall()
    conn.commit()
    product_list = []
    product_column =[]
    for i in range(len(product_select)):
        for j in range(len(product_select[i])):
            each_item=product_select[i][j]
            product_column.append(each_item)
        product_list.append(product_column)

    c.execute('SELECT door_pattern FROM door_pattern')
    door_pattern_select = c.fetchall()
    conn.commit()
    door_pattern_list = []
    door_pattern_column =[]
    for i in range(len(door_pattern_select)):
        for j in range(len(door_pattern_select[i])):
            each_item=product_select[i][j]
            door_pattern_column.append(each_item)
        door_pattern_list.append(door_pattern_column)

    c.execute('SELECT profile FROM profile')
    profile_select = c.fetchall()
    conn.commit()
    profile_list = []
    profile_column =[]
    for i in range(len(profile_select)):
        for j in range(len(profile_select[i])):
            each_item=profile_select[i][j]
            profile_column.append(each_item)
        profile_list.append(profile_column)

    c.execute('SELECT collection FROM collection')
    collection_select = c.fetchall()
    conn.commit()
    collection_list = []
    collection_column =[]
    for i in range(len(collection_select)):
        for j in range(len(collection_select[i])):
            each_item=collection_select[i][j]
            collection_column.append(each_item)
        collection_list.append(collection_column)  

    c.execute('SELECT highlight FROM highlight')
    highlight_select = c.fetchall()
    conn.commit()
    highlight_list = []
    highlight_column =[]
    for i in range(len(highlight_select)):
        for j in range(len(highlight_select[i])):
            each_item=highlight_select[i][j]
            highlight_column.append(each_item)
        highlight_list.append(highlight_column)


    c.execute("SELECT * FROM opr_data WHERE opr_id='{value1}'".format(value1=session["opr_id"]))
    opr_data_select = c.fetchall()
    conn.commit()
    opr_data_list = []
    opr_data_column =[]
    for i in range(len(opr_data_select)):
        for j in range(len(opr_data_select[i])):
            each_item=opr_data_select[i][j]
            opr_data_column.append(each_item)
        opr_data_list.append(opr_data_column)


    c.execute('SELECT room FROM room')
    room_select = c.fetchall()
    conn.commit()
    room_list = []
    room_column =[]
    for i in range(len(room_select)):
        for j in range(len(room_select[i])):
            each_item=room_select[i][j]
            room_column.append(each_item)
        room_list.append(room_column)

    c.execute("""SELECT customer_contact FROM customers WHERE customer_name='{value1}' """.format(value1=session["customer_opr"]))
    customer_contact_select=c.fetchall()
    session["customer_contact"]=customer_contact_select[0][0]

    c.execute("""SELECT customer_gst FROM customers WHERE customer_name='{value1}' """.format(value1=session["customer_opr"]))
    customer_gst_select=c.fetchall()
    session['customer_gst']=customer_gst_select[0][0]


    c.execute("SELECT highlight FROM opr_data WHERE opr_id='{value1}'".format(value1=opr_id))
    highlight_select_op = c.fetchall()
    conn.commit()
    highlight_list_op = []
    column =[]
    for i in range(len(highlight_select_op)):
        for j in range(len(highlight_select_op[i])):
            each_item=highlight_select_op[i][j]
            column.append(each_item)
        highlight_list_op.append(column)

    c.execute("SELECT kommandor_order_no FROM opr_data WHERE opr_id='{value1}'".format(value1=session["opr_id"]))
    kommandor_order_no_select = c.fetchall()
    conn.commit()
    kommandor_order_no_list = []
    column =[]
    for i in range(len(kommandor_order_no_select)):
        for j in range(len(kommandor_order_no_select[i])):
            each_item=kommandor_order_no_select[i][j]
            column.append(each_item)
        kommandor_order_no_list.append(column)

    if request.method=="POST":
        kommandor_order_no=request.form.get('kommandor_order_no')
        slido_order_no=request.form.get('slido_order_no')
        product=request.form.get('product')
        door_pattern=request.form.get('door_pattern')
        profile=request.form.get('profile')
        collection=request.form.get('collection')
        highlight=request.form.get('highlight')
        match_sample=request.form.get('match_sample')
        lock=request.form.get('lock')
        soft_close=request.form.get('soft_close')
        height=request.form.get('height')
        width=request.form.get('width')
        doors_per_set=request.form.get('doors_per_set')
        room=request.form.get('room')
        kommandor_basic_value=(request.form.get('kommandor_basic_value'))

        after_discount=float((session["discount"]))*int(str(kommandor_basic_value))
        gst=0.18*int(after_discount)
        final_price=gst+after_discount

        today = date.today()
        if request.form.get("add_order")=="add_order":
            c.execute("""INSERT INTO opr_data(opr_id,kommandor_order_no,slido_order_no,product,door_pattern,profile,collection,highlight,match_sample,lock,soft_close,height,width,doors_per_set,room,kommandor_basic_value,date,salesman_name,after_discount,gst,final_price) 
            VALUES('{value1}','{value2}','{value3}','{value4}','{value5}','{value6}','{value7}','{value8}','{value9}','{value10}','{value11}','{value12}','{value13}','{value14}','{value15}','{value16}','{value17}','{value18}','{value19}','{value20}','{value21}') """.format(value1=opr_id,value2=kommandor_order_no,value3=slido_order_no,value4=product,value5=door_pattern,value6=profile,value7=collection,value8=highlight,value9=match_sample,value10=lock,value11=soft_close,value12=height,value13=width,value14=doors_per_set,value15=room,value16=kommandor_basic_value,value17=today,value18=session["user"],value19=after_discount,value20=gst,value21=final_price))

    return render_template("new_opr_generation.html",product_list=product_list,door_pattern_list=door_pattern_list,profile_list=profile_list,collection_list=collection_list,highlight_list=highlight_list,room_list=room_list,opr_data_list=opr_data_list)
        
if __name__ == '__main__':
    app.run(debug=True)