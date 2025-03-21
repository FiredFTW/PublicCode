from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, timedelta
from db import get_db
import os

# Get the current directory of the Python script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to the SQLite database file relative to the current directory
DATABASE_FILE = os.path.join(current_directory, 'db_tables.sql')


app = Flask(__name__, instance_relative_config=True)
app.config['DATABASE'] = DATABASE_FILE
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

import db
db.init_app(app)

import auth 
app.register_blueprint(auth.bp)

import kitchen
app.register_blueprint(kitchen.bp)

import menu
app.register_blueprint(menu.bp)

@app.route('/home_page')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('home.html', tables=range(1, 7))

# Route for the menu page
@app.route('/order/<int:table_id>', methods=['GET'])
def order(table_id):
    #db = get_db()
    #mains = db.execute('SELECT * FROM mains').fetchall()
    #appertizers = db.execute('SELECT * FROM appertizers').fetchall()
    #desserts = db.execute('SELECT * FROM desserts').fetchall()
    #sides = db.execute('SELECT * FROM sides').fetchall()
    #drinks = db.execute('SELECT * FROM drinks').fetchall()
    #db.close()

    # Organize the menu items by categories
    #menu_items = {
    #    'Mains': mains,
    #    'Appertizers': appertizers,
    #    'Desserts': desserts,
    #    'Sides': sides,
    #    'Drinks': drinks
    #}
    
    return render_template('menu.html', table_id=table_id)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    table_number = request.form.get('table_id')
    notes = request.form.get('notes')
    listofItems = request.form.get('selectedItems')
    listofItems = listofItems.split(",")
    x = 0
    while x < len(listofItems):
        if database_insert(listofItems[x], listofItems[x + 1], table_number) == False:
            return redirect(url_for("home"))    
        else:
            x = x + 2
    return redirect(url_for('basket', table_id = table_number))
    

def database_insert(item, category, table_number):
    try:     
        # Connect to the database
        db = get_db()
        # Check if an order for the table number already exists
        existing_order = db.execute(
            'SELECT * FROM orders WHERE table_num = ?', (table_number,)
        ).fetchone()
        if existing_order:
            if existing_order[category] == None:
                combined_items = item
            else:
                combined_items = existing_order[category] + ", " + item
            # Update the existing order with the combined items
            db.execute(
                f'UPDATE orders SET {category} = ? WHERE table_num = ?',
                (combined_items, table_number)
            )
        else:
            # Insert a new order into the database
            db.execute(
                f'INSERT INTO orders (table_num, waiter_id, {category}) VALUES (?, ?, ?)',
                (table_number, 1, item )
            )
        db.commit()
        flash(f'{category.capitalize()} added to order successfully!')
        return True

    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return False    


@app.route('/kitchen', methods=['GET', 'POST'])
def kitchen():
    search_query = request.args.get('search', '')
    current_time = datetime.utcnow()
    
    # Connect to the database
    db = get_db()

    # Query the orders table to retrieve current orders
    cur = db.execute('SELECT * FROM orders')
    orders = cur.fetchall()
    
    # Close the database connection
    db.close()

    # Process orders to determine priority color
    for order in orders:
        order_time = order['timestamp']
        time_diff = current_time - order_time
        if time_diff <= timedelta(minutes=15):
            order['priority_color'] = 'green'
        elif timedelta(minutes=15) < time_diff <= timedelta(minutes=30):
            order['priority_color'] = 'amber'
        else:
            order['priority_color'] = 'red'
    
    # Filter orders based on search query
    filtered_orders = [order for order in orders if search_query.lower() in str(order['table_num']).lower() or search_query.lower() in " ".join(item.lower() for item in order['order_items'])]
    
    return render_template('kitchen_ui.html', orders=filtered_orders, search_query=search_query)

@app.route('/mark_as_completed/<int:order_id>', methods=['POST'])
def mark_as_completed(order_id):
    try:
        orders[order_id]['status'] = 'COMPLETED'
        orders[order_id]['completed'] = True
        orders[order_id]['completed_time'] = datetime.utcnow()  # Storing the completion time
    except IndexError:
        pass  # Handle the error
    return redirect(url_for('kitchen'))


@app.route('/completed_orders')
def view_completed_orders():
    return render_template('completed_orders.html', completed_orders=completed_orders)


@app.route('/remove_order/<int:order_id>', methods=['POST'])
def remove_order(order_id):
    try:
        if orders[order_id]['completed']:
            completed_orders.append(orders[order_id])  # Move to completed orders list
            del orders[order_id]
    except IndexError:
        pass  # Handle the error
    return redirect(url_for('kitchen'))

@app.route('/mark_for_pickup/<int:order_id>', methods=['POST'])
def mark_for_pickup(order_id):
    try:
        orders[order_id]['ready_for_pickup'] = True
        # Logic to notify waiter goes here, e.g., push notification, etc.
    except IndexError:
        pass  # Handle the error appropriately
    return redirect(url_for('kitchen'))

waiterCalledTables = ["No tables needed assisting"]

@app.route('/call_waiter', methods=['POST'])
def call_waiter():
    if request.method == 'POST':
        table_id = request.json.get('table_id')
        if table_id is not None:
            waiterCalledTables.append(f"Table {table_id} requests assistance")
            print(waiterCalledTables)
            return jsonify({"message": f"A waiter has been called to take food to table {table_id}"})
        else:
            return jsonify({"error": "Table ID not provided"}), 400

#Route for the basket.
@app.route('/basket/<int:table_id>', methods=['GET','POST'])
def basket(table_id):
    db = get_db()
    try:
        basket = db.execute(f'SELECT * FROM orders WHERE table_num = {table_id}').fetchone()
        db.commit() 
        #Menu list to be put through the total_calc function.
        menu = ['appertizers', 'mains', 'desserts', 'sides', 'drinks']
        total_cost = 0

        #If there is an order with the table number it will render the basket html page.
        if basket:
        #Loop through all the menu item results from the sql query.
            for i in range(2,7):
                if basket[i] is not None and basket[i] != "":
                    total_cost += total_calc(basket[i], menu[i - 2]) 
            total_cost = round(total_cost, 2)
            return render_template('basket.html', basket=basket, total=total_cost)
         
        #If there isnt an order with the table number it will redirect to the mains page of the menu and give a message that no order has been placed.
        else:
            flash("No Orders submitted yet.")
            return redirect(url_for('order', table_id = table_id))
        
    #If the sql query messes up or any unknown exceptions occur it will be redirect to the mains page of the menu.
    except Exception as e:
        print(str(e))
        flash(f"An error occured: {str(e)}")
        return redirect(url_for('order', table_id = table_id))

#Created a seperate function for calculating the total_cost to remove repeated code.
def total_calc(items, menu_item):
    db = get_db()
    total_cost = 0 

    if len(items.split(" ")) == 1:
        cost = db.execute(f'SELECT cost FROM {menu_item} WHERE title= ?', (items,)).fetchone()
        total_cost += cost[0]
        db.commit()
        return total_cost
    #Have to split the items up as they come as a long string.
    for item in items.split(", "):
            cost = db.execute(f'SELECT cost FROM {menu_item} WHERE title= ?', (item,)).fetchone()
            total_cost += cost[0]
            db.commit()
    return total_cost

@app.route('/basket_removeAll/<int:table_id>', methods=['GET','POST'])
def basket_removeAll(table_id):
    db = get_db()
    try:
        db.execute(f'DELETE FROM orders WHERE table_num = {table_id}')
        db.commit()  
        return redirect(url_for('home'))
    except Exception as e:
        print(str(e))
        flash(f"An error occured: {str(e)}")
        return redirect(url_for('home'))

@app.route('/remove_call_waiter', methods=['POST'])
def remove_call_waiter_message():
    if request.method == 'POST':
        # Remove the last item from the array as it's just a holding value for now
        if waiterCalledTables:
            waiterCalledTables.pop()
        print(waiterCalledTables)  # Print to check to ensure that the message removed
        return jsonify({"message": "Waiter has been informed you no longer need assistance"})
    
@app.route('/select_table', methods=['POST'])
def select_table():
    # Redirect to the home page
    return redirect('/')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

