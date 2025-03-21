import functools
from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for )
from db import get_db

#Blueprint created for all of the menu items. Name of BP is called menu and in the url it will be in directory /menu.
bp = Blueprint('menu', __name__, url_prefix='/menu')

@bp.route('/add-specific-item/<item_type>', methods=['GET', 'POST'])
def add_specific_item(item_type):
    if request.method == 'POST':
        if item_type == 'appetizer':
            # Extract form data for appetizer
            title = request.form['title']
            vegan = request.form['vegan']
            gluten_free = request.form['gluten_free']
            vegetarian = request.form['vegetarian']
            nuts_free = request.form['nuts_free']
            cost = request.form['cost']

            db = get_db()
            # Check if the appetizer title already exists to avoid duplicates
            existing_appetizer = db.execute('SELECT 1 FROM appetizers WHERE title = ?', (title,)).fetchone()

            if existing_appetizer:
                flash('Appetizer with this title already exists!', 'error')
            else:
                # Insert the new appetizer into the database
                db.execute('INSERT INTO appertizers (title, vegan, gluten_free, vegetarian, nuts_free, cost) VALUES (?, ?, ?, ?, ?, ?)',
                        (title, vegan, gluten_free, vegetarian, nuts_free, cost))
                db.commit()
                flash('New appetizer added successfully!')

        elif item_type == 'drink':
            title = request.form['title']
            cost = request.form['cost']
            
            db = get_db()

            existing_drink = db.execute('SELECT 1 FROM drinks WHERE title = ?', (title,)).fetchone()

            if existing_drink:
                flash('Drink with this title already exists!', 'error')
                
            else:
                db.execute('INSERT INTO drinks (title, cost) VALUES (?, ?)', (title, cost))
                db.commit()
                flash('New drink added successfully!')

        if item_type == 'dessert':
            title = request.form['title']
            vegan = request.form['vegan']
            gluten_free = request.form['gluten_free']
            vegetarian = request.form['vegetarian']
            nuts_free = request.form['nuts_free']
            cost = request.form['cost']

            db = get_db()

            existing_dessert = db.execute('SELECT * FROM desserts WHERE title = ?', (title,)).fetchone()
            
            if existing_dessert:
                flash(f'A dessert with the title "{title}" already exists.', 'error')
            else:
                db.execute('INSERT INTO desserts (title, vegan, gluten_free, vegetarian, nuts_free, cost) VALUES (?, ?, ?, ?, ?, ?)',
                           (title, vegan, gluten_free, vegetarian, nuts_free, cost))
                db.commit()
                flash('New dessert added successfully!')
        
        elif item_type == 'side_dish':
            title = request.form['title']
            vegan = request.form['vegan']
            gluten_free = request.form['gluten_free']
            vegetarian = request.form['vegetarian']
            nuts_free = request.form['nuts_free']
            cost = request.form['cost']

            db = get_db()
            
            existing_side = db.execute('SELECT 1 FROM sides WHERE title = ?', (title,)).fetchone()

            if existing_side:
                flash('Side dish with this title already exists!', 'error')
            else:
                db.execute('INSERT INTO sides (title, vegan, gluten_free, vegetarian, nuts_free, cost) VALUES (?, ?, ?, ?, ?, ?)',
                        (title, vegan, gluten_free, vegetarian, nuts_free, cost))
                db.commit()
                flash('New side dish added successfully!')
                        
        elif item_type == 'main_course':
            title = request.form['title']
            vegan = request.form['vegan']
            gluten_free = request.form['gluten_free']
            vegetarian = request.form['vegetarian']
            nuts_free = request.form['nuts_free']
            cost = request.form['cost']

            db = get_db()            

            existing_main = db.execute('SELECT 1 FROM mains WHERE title = ?', (title,)).fetchone()

            if existing_main:
                flash('Main course with this title already exists!', 'error')
            else:
                db.execute('INSERT INTO mains (title, vegan, gluten_free, vegetarian, nuts_free, cost) VALUES (?, ?, ?, ?, ?, ?)',
                           (title, vegan, gluten_free, vegetarian, nuts_free, cost))
                db.commit()
                flash('New main course added successfully!')


        return redirect(url_for('menu.add_item'))

    return render_template(f'add_{item_type}.html')


@bp.route('/add-item', methods=['GET', 'POST'])
def add_item():
    # Drop-down listing type of menu items
    # point is to use the selection as an index by which to search the database
    item_types = ['Appetizer', 'Main Course', 'Dessert', 'Side Dish', 'Drink']
    if request.method == 'POST':
        selected_type = request.form['item_type'].lower().replace(" ", "_")  # Convert to lowercase and underscores for consistency
        # Redirect to a route that handles adding a specific type of item
        return redirect(url_for('menu.add_specific_item', item_type=selected_type))
    return render_template('add_item.html', item_types=item_types)


#Route for the mains html page.
@bp.route('/mains', methods=['GET'])
def mains():
   db = get_db()
   mains = db.execute('Select * FROM mains').fetchall()
   db.commit()
   #Table id will be implemented from the tables table in the database once the customer has sleected thier table. 
   #From there we can use Ivan's code which will store it through each html page so when customer comes to order they do not have to enter table num again. 
   table_id = 1
   db.close()
   #You have to pass the mains into the render template function for the html page to use.
   return render_template('mains.html', mains=mains, table_id=table_id)

#Route to the appertizers html page.
@bp.route('/appertizers', methods=['GET'])
def appertizers():
   db = get_db()
   appertizers = db.execute('Select * FROM appertizers').fetchall()
   db.commit()
   return render_template('appertizers.html', appertizers=appertizers)

#Route to the desserts html page.
@bp.route('/desserts', methods=['GET'])
def desserts():
   db = get_db()
   desserts = db.execute('Select * FROM desserts').fetchall()
   db.commit()
   return render_template('desserts.html', desserts=desserts)

#Route to the sides html page.
@bp.route('/sides', methods=['GET'])
def sides():
   db = get_db()
   sides = db.execute('Select * FROM sides').fetchall()
   db.commit()
   db.close()
   return render_template('sides.html', sides=sides)

#Route to the drinks html page.
@bp.route('/drinks', methods=['GET'])
def drinks():
   db = get_db()
   drinks = db.execute('Select * FROM drinks').fetchall()
   db.commit()
   db.close()
   return render_template('drinks.html', drinks=drinks)

from flask import request

from flask import request

from flask import request

@bp.route('/add_to_order/<item_type>', methods=['POST'])
def add_to_order(item_type):
    try:
        # Retrieve the table number and selected items from the form data
        table_number = request.form['table_number']
        selected_items = request.form.getlist(f'selected_{item_type}[]')

        # Connect to the database
        db = get_db()

        # Check if an order for the table number already exists
        existing_order = db.execute(
            'SELECT * FROM orders WHERE table_num = ?', (table_number,)
        ).fetchone()

        if existing_order:
            # Retrieve the existing items from the database
            existing_items = existing_order[item_type].split(', ') if existing_order[item_type] else []

            # Combine the existing items with the selected items
            combined_items = existing_items + selected_items

            # Remove duplicates and empty strings
            combined_items = list(filter(None, set(combined_items)))

            # Update the existing order with the combined items
            db.execute(
                f'UPDATE orders SET {item_type} = ? WHERE table_num = ?',
                (', '.join(combined_items), table_number)
            )
        else:
        # Insert a new order into the database
            db.execute(
            f'INSERT INTO orders (table_num, waiter_id, {item_type}) VALUES (?, ?, ?)',
            (table_number, 1, ', '.join(selected_items))
            )

        db.commit()
        flash(f'{item_type.capitalize()} added to order successfully!')
        return redirect(url_for(f"menu.{item_type}"))

    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for(f"menu.{item_type}"))


#Route for tthe basket.
@bp.route('/basket', methods=['GET','POST'])
def basket():
    db = get_db()
    try:
        #Will need something like this later on for the table number when they select it.
        #table_number = request.form['table_number']   
        #basket = db.execute(f'Select * FROM orders where table_num = ?', (table_number))

        basket = db.execute('SELECT * FROM orders WHERE table_num = 1').fetchone()
        db.commit()
        
        #Menu list to be put through the total_calc function.
        menu = ['appertizers', 'mains', 'desserts', 'sides', 'drinks']
        total_cost = 0

        #Loop through all the menu item results from the sql query.
        for i in range(2,7):
            if basket[i] is not None:
                total_cost += total_calc(basket[i], menu[i -2])        
        
        #If there is an order with the table number it will render the basket html page.
        if basket:
            return render_template('basket.html', basket=basket, total=total_cost)
         
        #If there isnt an order with the table number it will redirect to the mains page of the menu and give a message that no order has been placed.
        else:
            flash("No Orders submitted yet.")
            return redirect(url_for('menu.mains'))
        
    #If the sql query messes up or any unknown exceptions occur it will be redirect to the mains page of the menu.
    except Exception as e:
        flash(f"An error occured: {str(e)}")
        return redirect(url_for('menu.mains'))

#Created a seperate function for calculating the total_cost to remove repeated code.
def total_calc(items, menu_item):
    db = get_db()
    total_cost = 0 
    #Have to split the items up as they come as a long string.
    for item in items.split(", "):
            cost = db.execute(f'SELECT cost FROM {menu_item} WHERE title= ?', (item,)).fetchone()
            total_cost += cost[0]
            db.commit()
    return total_cost

