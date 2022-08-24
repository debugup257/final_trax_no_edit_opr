from flask import Flask, render_template, render_template_string, request,redirect,url_for,session
import psycopg2
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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
        product_id = request.form.get("product_id")
        product_name = request.form.get("product_name")
        product_height = request.form.get("product_height")
        product_width = request.form.get("product_width")
        product_weight = request.form.get("product_weight")
        product_cost = request.form.get("product_cost")
        product_mrp = request.form.get("product_mrp")
        product_description = request.form.get("product_description")
        c.execute("""UPDATE users SET product_id='{value1}',product_name='{value2}',product_height='{value3},product_height='{value4},product_weight='{value5},product_cost='{value6},product_mrp='{value7},product_description='{value8}' WHERE product_id='{value9}'""".format(value1=product_id,value2=product_name,value3=product_height,value4=product_width,value5=product_weight,value6=product_cost,value7=product_mrp,value8=product_description,value9=product_id_to_edit ))
        conn.commit()
        session.pop('product_id_to_edit')

        return redirect(url_for("new_product", product=product_list))
    return render_template("product_edit.html")

    

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

            customer_id=request.form.get('customer_id')
            customer_name=request.form.get('customer_name')
            customer_address=request.form.get('customer_address')
            customer_type=request.form.get('customer_type')
            customer_gst=request.form.get('customer_gst')
            customer_contact=request.form.get('customer_contact')
            c.execute("INSERT INTO customers(customer_id) VALUES('{value}')".format(value=customer_id))
            conn.commit()
            c.execute("UPDATE customers SET customer_name={value1} WHERE customer_id={value2}".format(value1=customer_name, value2=customer_id))
            conn.commit
            c.execute("UPDATE customers SET customer_address={value1} WHERE customer_id={value2}".format(value1=customer_address, value2=customer_id))
            conn.commit
            c.execute("UPDATE customers SET customer_type={value1} WHERE customer_id={value2}".format(value1=customer_type, value2=customer_id))
            conn.commit
            c.execute("UPDATE customers SET customer_gst={value1} WHERE customer_id={value2}".format(value1=customer_gst, value2=customer_id))
            conn.commit
            c.execute("UPDATE customers SET customer_contact={value1} WHERE customer_id={value2}".format(value1=customer_contact, value2=customer_id))
            conn.commit

        if request.form.get("edit")=="edit":
            session['customer_id_to_edit'] = request.form.get("customer_id_table")
            return redirect(url_for("customer_edit"))
        return render_template("new_customer.html", data=customers)
   return render_template("index.html")





if __name__ == '__main__':
    app.run(debug=True)