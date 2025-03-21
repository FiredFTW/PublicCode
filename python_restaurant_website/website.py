from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, timedelta
#from db import get_db
import os


website = Flask(__name__)

waiterCalledTables = ["No tables needed assisting"]

@website.route('/')
def index():
    return render_template('menu.html')

@website.route('/call_waiter', methods=['POST'])
def call_waiter():
    if request.method == 'POST':
        waiterCalledTables.append("Table x requests assistance")#Using x at the moment while the selecting table is unadded within this code
        print(waiterCalledTables)
        return jsonify({"message": "A waiter has been called to your table"})
    
@website.route('/remove_call_waiter', methods=['POST'])
def remove_call_waiter_message():
    if request.method == 'POST':
        # Remove the last item from the array as it's just a holding value for now
        if waiterCalledTables:
            waiterCalledTables.pop()
        print(waiterCalledTables)  # Print to check to ensure that the message removed
        return jsonify({"message": "Waiter has been informed you no longer need assistance"})
    
@website.route('/select_table')
def select_table():
    return redirect(url_for('appivan.py'))
    
if __name__ == '__main__':
    website.run(host='0.0.0.0', port=5003, debug=True) ##Done in order to have a different IP to the first test I did.

