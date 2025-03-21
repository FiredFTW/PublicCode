import functools
from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for )
from db import get_db

bp = Blueprint('kitchen', __name__, url_prefix='/kitchen')

#Route for the orders html page.
@bp.route('/orders', methods=['GET'])
def orders():
    # Connect to the database
    db = get_db()

    # Query the orders table to retrieve current orders
    cur = db.execute('SELECT * FROM orders')
    orders = cur.fetchall()
    db.commit()

    # Render the template with the orders data
    return render_template('orders.html', orders=orders)

@bp.route('/insert_orders', methods=['GET'])
def insert_orders():
    # Connect to the database
    try:
         
        db = get_db()

        # Query the orders table to retrieve current orders
        db.execute('''INSERT INTO orders (table_num, waiter_id, appertizers, mains, desserts, sides, drinks, notes)
    VALUES
        (1, 1, 'Prawns', 'Hot dog', 'Ice Cream', 'Fries', 'Coke', 'No nuts for dessert'),
        (2, 2, 'Cheesy Garlic Bread', 'Burger', 'Chocolate Cake', 'Onion rings', 'Lemonade', 'No onions in the burger'),
        (3, 1, 'Prawns', 'Hot dog', 'Chocolate Cake', 'Fries', 'Coke', 'Extra ketchup');
    ''')
        db.commit()
        return redirect(url_for('kitchen.orders'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('kitchen.orders'))

@bp.route('/remove_order', methods=['POST'])
def remove_order():
    try:
        # Connect to the database
        db = get_db()

        # Get the order ID from the form data
        order_id = request.form['order_id']

        # Delete the order from the database
        db.execute('DELETE FROM orders WHERE table_num = ?', (order_id,))
        db.commit()

        # Redirect to the orders page or any other appropriate page
        return redirect(url_for('kitchen.orders'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('kitchen.orders'))
