
route_name = "new_highlight"
list_columns = ["opr_id","customer_opr","delivery_address","preferred_delivery_time","cargo_vehicle_time","floor_number","lift_available" ]
table_name ="customer_opr"
pkey_of_table ="highlight_id"
edit_page="highlight_edit"

print("""@app.route('/{route_name}', methods=['GET','POST'])
def {route_name}():
    
    
   if "user" in session:
        c.execute('SELECT * FROM {table_name}')
        {table_name}_select = c.fetchall()
        conn.commit()
        {table_name} = []
        column =[]
        for i in range(len({table_name}_select)):
            for j in range(len({table_name}_select[i])):
                each_item={table_name}_select[i][j]
                column.append(each_item)
            {table_name}.append(column)
    
        if request.method=="POST":
            if request.form.get("delete")=="delete":
                to_delete=request.form.get("{pkey_of_table}_table")
                c.execute("DELETE FROM {table_name} WHERE {pkey_of_table}='{{to_delete}}'".format(to_delete=to_delete))
                conn.commit()
    
        if request.form.get("create")=="create":
            for i in range(len({table_name})):
                {table_name}[i] = request.form.get("{table_name}[i]")
                c.execute("INSERT INTO {table_name}({table_name}[i]) VALUES('{table_name}[i]')".format({table_name}[i]={table_name}[i]))
                conn.commit()

        if request.form.get("edit")=="edit":
            session['{pkey_of_table}_to_edit'] = request.form.get("{pkey_of_table}_table")
            return redirect(url_for("{edit_page}"))
        return render_template("{route_name}.html", data={table_name})
   return render_template("index.html")

    """.format(route_name =route_name ,list_columns =list_columns , table_name =table_name, pkey_of_table =pkey_of_table,edit_page=edit_page)
)

# ***********edit page**********************

print("""@app.route('/{edit_page}', methods=['GET','POST'])
def {edit_page}():

{pkey_of_table}_to_edit=session['{pkey_of_table}_to_edit']

c.execute('SELECT * FROM {table_name}')
{table_name}_select = c.fetchall()
conn.commit()
{table_name}_list = []
column =[]
for i in range(len({table_name}_select)):
    for j in range(len({table_name}_select[i])):
        each_item={table_name}_select[i][j]
        column.append(each_item)
    {table_name}_list.append(column)
if request.method=="POST":

        conn.commit()
        session.pop('{pkey_of_table}_to_edit')
        return redirect(url_for("{route_name}", data={table_name}_list))
return render_template("{edit_page}.html")
""".format(route_name =route_name ,list_columns =list_columns , table_name =table_name, pkey_of_table =pkey_of_table,edit_page=edit_page))



# ******************get items from html****************

# create
for i in range(len(list_columns)):
    print(list_columns[i],"=request.form.get(","'",list_columns[i],"'",")",sep="" )
print('c.execute("INSERT INTO ',table_name,"(",list_columns[0],") VALUES('","{value}","')",'".format(value=',list_columns[0],"))",sep="")
print("conn.commit()")



# edit
for i in range(len(list_columns)):
    print(list_columns[i],"=request.form.get(","'",list_columns[i],"_edit","'",")",sep="" )



# *******************************sql command*******************************

print("create table ",table_name,"(",list_columns[0],"varchar primary key,")
a=list_columns.copy()
del a[0]
for i in range(len(a)):
    print(a[i],"varchar,")
print(");")
# remove the last comma