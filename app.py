from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)#יצירת מופע של אפליקציית פלאסק
app.secret_key = 'your_secret_key'#מגדירים מפתח סודי לשימוש מערכת הסשן
DATABASE = 'users.db'#שימוש במסד נתונים 

def get_db_connection():
    conn = sqlite3.connect(DATABASE)#חיבור למסד נתונים
    conn.row_factory = sqlite3.Row#מגדירים את השורות כמילון כדי שנוכל לגשת לנתונים בעזרת מפתחות
    return conn#מחזירים את החיבור למסד

def init_db():
    conn = get_db_connection()#חיבור למסד נתונים
    cursor = conn.cursor()#יצירת אובייקט מצביע לביצוע פעולות במסד נתונים
 #  ביצוע פקודות ס.ק.ל ליצירת טבלת משתמשים אם היא לא קיימת כאשר חובה לשים אימייל , סיסמא והמשתמש הדיפולטיבי הוא יוזר
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        name TEXT,
        surname TEXT,
        city TEXT,
        address TEXT,
        birth_date TEXT,
        role TEXT NOT NULL DEFAULT 'USER'
    )
    ''')
# id ביצוע פקודות ס.ק.ל ליצירת טבלת עגלה אם היא לא קיימת כאשר הטבלה מתחברת לטבלת משתמשים בעזרת מפתח משתמש
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        dish_name TEXT,
        restaurant_name TEXT,
        dish_price REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
# id ביצוע פקודות ס.ק.ל ליצירת טבלת הזמנות אם היא לא קיימת כאשר הטבלה מתחברת לטבלת משתמשים בעזרת מפתח משתמש
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_name TEXT,
        dish_name TEXT,
        restaurant_name TEXT,
        dish_price REAL,
        special_requests TEXT,
        status TEXT NOT NULL DEFAULT 'Pending',
        order_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    conn.commit()#אישור כל השינויים שנעשו במסד במהלך ההתחברות הנוכחית
    conn.close()#סגירת החיבור למסד

def create_dishes_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT NOT NULL,
            restaurant_name TEXT NOT NULL
        )
    ''')

def create_recommendations_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_name TEXT NOT NULL,
            user_name TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            comment TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_sample_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM dishes')
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute('''
             INSERT INTO dishes (name, description, price, image_url, restaurant_name)
    VALUES 
    ('Spaghetti Carbonara', 'Creamy pasta with crispy pancetta, grated Parmesan cheese, and fresh parsley.', 14.99, 'images/spaghetti_carbonara.jpg', 'Italian Bistro'),
    ('Margherita Pizza', 'Crispy crust topped with fresh tomatoes, mozzarella cheese, and basil leaves.', 12.99, 'images/margherita_pizza.jpg', 'Italian Bistro'),
    ('Tiramisu', 'Layers of coffee-soaked ladyfingers, mascarpone cheese, and cocoa powder.', 6.99, 'images/tiramisu.jpg', 'Italian Bistro'),
    ('Kung Pao Chicken', 'A spicy, flavorful dish with tender chicken, bell peppers, peanuts, and scallions in a glossy sauce.', 12.99, 'images/kung_pao_chicken.jpg', 'Chinese Food'),
    ('Sweet and Sour Pork', 'Crispy fried pork pieces in a vibrant sauce made from pineapple, bell peppers, and onions.', 10.99, 'images/sweet_and_sour_pork.jpg', 'Chinese Food'),
    ('Beef and Broccoli', 'Tender beef strips and fresh broccoli florets stir-fried in a savory garlic and ginger soy sauce.', 11.99, 'images/beef_and_broccoli.jpg', 'Chinese Food'),
    ('Tacos al Pastor', 'Marinated pork, pineapple, cilantro, and onions in soft corn tortillas. Spicy and flavorful.', 9.99, 'images/tacos_al_pastor.jpg', 'Mexican Fiesta'),
    ('Chicken Enchiladas', 'Tortillas filled with shredded chicken, topped with a rich red sauce, melted cheese, and fresh cilantro.', 11.99, 'images/chicken_enchiladas.jpg', 'Mexican Fiesta'),
    ('Churros', 'Crispy fried dough coated in cinnamon sugar, served with a side of rich chocolate dipping sauce.', 5.99, 'images/churros.jpg', 'Mexican Fiesta'),
    ('Sushi Platter', 'Various types of sushi rolls with fresh fish, avocado, and vegetables, garnished with pickled ginger and wasabi.', 18.99, 'images/sushi_platter.jpg', 'Sushi Heaven'),
    ('Ramen', 'Rich broth, noodles, sliced pork, soft-boiled egg, and green onions. Comforting and appetizing.', 12.99, 'images/ramen.jpg', 'Sushi Heaven'),
    ('Mochi Ice Cream', 'Small round rice cakes filled with different flavors of ice cream. Colorful and refreshing.', 6.99, 'images/mochi_ice_cream.jpg', 'Sushi Heaven')
        ''')
        conn.commit()
    conn.close()

init_db()
create_dishes_table()
create_recommendations_table()

def send_email(to_email, subject, body):
    from_email = "your_email@example.com"
    from_password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_dish_by_id(dish_id):
    conn = get_db_connection()
    dish = conn.execute('SELECT * FROM dishes WHERE id = ?', (dish_id,)).fetchone()
    conn.close()
    if dish:
        return dict(dish)
    return None

def update_dish(dish_id, form_data):
    conn = get_db_connection()
    conn.execute('''
        UPDATE dishes
        SET name = ?, description = ?, price = ?, image_url = ?
        WHERE id = ?
    ''', (form_data['name'], form_data['description'], form_data['price'], form_data['image_url'], dish_id))
    conn.commit()
    conn.close()

def create_dish(restaurant_name, form_data):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO dishes (name, description, price, image_url, restaurant_name)
        VALUES (?, ?, ?, ?, ?)
    ''', (form_data['name'], form_data['description'], form_data['price'], form_data['image_url'], restaurant_name))
    conn.commit()
    conn.close()

def delete_dish(dish_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM dishes WHERE id = ?', (dish_id,))
    conn.commit()
    conn.close()

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    surname = request.form['surname']
    city = request.form['city']
    address = request.form['address']
    birth_date = request.form['birth_date']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (email, password, name, surname, city, address, birth_date, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'USER')
        ''', (email, password, name, surname, city, address, birth_date))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "User with this email already exists!"
    conn.close()
    return redirect(url_for('login_page'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        session['user_name'] = f"{user[3]} {user[4]}"
        session['role'] = user[8]
        if session['role'] == 'ADMIN':
            return redirect(url_for('admin_homepage'))
        elif session['role'] == 'OPERATOR':
            return redirect(url_for('operator_homepage'))
        else:
            return redirect(url_for('user_homepage'))
    else:
        return "Invalid credentials!"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('role', None)
    return redirect(url_for('welcome'))

@app.route('/upgrade_user/<int:user_id>', methods=['POST'])
def upgrade_user(user_id):
    if 'user_id' not in session or session['role'] != 'ADMIN':
        return "Access denied!"

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = 'OPERATOR' WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

@app.route('/users')
def users():
    if 'user_id' not in session or session['role'] != 'ADMIN':
        return "Access denied!"

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, name, surname, city, address, birth_date, role FROM users')
    users = cursor.fetchall()
    conn.close()

    return render_template('users.html', users=users)

@app.route('/add_admin')
def add_admin():
    email = 'admin2@example.com'
    password = 'adminpassword'
    name = 'Admin'
    surname = 'User'
    city = 'AdminCity'
    address = 'AdminAddress'
    birth_date = '2000-01-01'
    role = 'ADMIN'

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (email, password, name, surname, city, address, birth_date, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email, password, name, surname, city, address, birth_date, role))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "Admin user already exists!"
    conn.close()
    return "Admin user created successfully!"

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or session['role'] != 'ADMIN':
        return "Access denied!"

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.html')

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    if session['role'] in ['ADMIN', 'OPERATOR']:
        orders = conn.execute('''
            SELECT order_id, user_name, GROUP_CONCAT(dish_name, ', ') as dishes, GROUP_CONCAT(restaurant_name, ', ') as restaurants, 
                   SUM(dish_price) as total_price, special_requests, status
            FROM orders
            GROUP BY order_id, user_name, special_requests, status
        ''').fetchall()
    else:
        orders = conn.execute('''
            SELECT order_id, user_name, GROUP_CONCAT(dish_name, ', ') as dishes, GROUP_CONCAT(restaurant_name, ', ') as restaurants, 
                   SUM(dish_price) as total_price, special_requests, status
            FROM orders
            WHERE user_id = ?
            GROUP BY order_id, user_name, special_requests, status
        ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/restaurant/<restaurant_name>')
def restaurant_menu(restaurant_name):
    conn = get_db_connection()
    dishes = conn.execute('SELECT * FROM dishes WHERE restaurant_name = ?', (restaurant_name.replace("_", " ").title(),)).fetchall()
    conn.close()
    return render_template(f'{restaurant_name}.html', dishes=dishes, restaurant_name=restaurant_name.replace("_", " ").title())

@app.route('/admin_homepage')
def admin_homepage():
    return render_template('admin_homepage.html')

@app.route('/operator_homepage')
def operator_homepage():
    return render_template('operator_homepage.html')

@app.route('/user_homepage')
def user_homepage():
    return render_template('user_homepage.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    user_id = session['user_id']
    dish_name = request.form['dish_name']
    restaurant_name = request.form['restaurant_name']
    dish_price = float(request.form['dish_price'])

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cart (user_id, dish_name, restaurant_name, dish_price) VALUES (?, ?, ?, ?)', (user_id, dish_name, restaurant_name, dish_price))
    conn.commit()
    conn.close()

    return redirect(request.referrer)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    user_id = session['user_id']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, dish_name, restaurant_name, dish_price FROM cart WHERE user_id = ?', (user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    total = sum(item[3] for item in cart_items)

    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/delete_from_cart/<int:item_id>', methods=['POST'])
def delete_from_cart(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    user_id = session['user_id']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE id = ? AND user_id = ?', (item_id, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('cart'))

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    user_id = session['user_id']
    user_name = session['user_name']
    special_requests = request.form.get('special_requests', '')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(order_id) FROM orders')
    max_order_id = cursor.fetchone()[0]
    next_order_id = (max_order_id + 1) if max_order_id else 1

    cursor.execute('SELECT dish_name, restaurant_name, dish_price FROM cart WHERE user_id = ?', (user_id,))
    cart_items = cursor.fetchall()

    for item in cart_items:
        cursor.execute('''
            INSERT INTO orders (user_id, user_name, dish_name, restaurant_name, dish_price, special_requests, status, order_id)
            VALUES (?, ?, ?, ?, ?, ?, 'Pending', ?)
        ''', (user_id, user_name, item[0], item[1], item[2], special_requests, next_order_id))

    cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('cart'))

@app.route('/mark_complete/<int:order_id>', methods=['POST'])
def mark_complete(order_id):
    if 'user_id' not in session or session['role'] not in ['ADMIN', 'OPERATOR']:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    order = conn.execute('SELECT user_id FROM orders WHERE order_id = ?', (order_id,)).fetchone()
    if order:
        user_id = order['user_id']
        user = conn.execute('SELECT email FROM users WHERE id = ?', (user_id,)).fetchone()
        if user:
            user_email = user['email']
            subject = "Your Order Has Been Approved"
            body = f"Your order with order ID {order_id} has been approved. Thank you for ordering with us!"
            send_email(user_email, subject, body)

    conn.execute('UPDATE orders SET status = ? WHERE order_id = ?', ('Completed', order_id))
    conn.commit()
    conn.close()
    return redirect(url_for('orders'))

@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    if 'user_id' not in session or session['role'] not in ['ADMIN', 'OPERATOR']:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    conn.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('orders'))

@app.route('/home')
def home():
    role = session.get('role')
    if role == 'ADMIN':
        return redirect(url_for('admin_homepage'))
    elif role == 'OPERATOR':
        return redirect(url_for('operator_homepage'))
    elif role == 'USER':
        return redirect(url_for('user_homepage'))
    else:
        return redirect(url_for('login_page'))

@app.route('/edit_dish/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(dish_id):
    if session.get('role') != 'ADMIN':
        return redirect(url_for('login_page'))
    dish = get_dish_by_id(dish_id)
    if dish is None:
        return "Dish not found", 404

    if request.method == 'POST':
        update_dish(dish_id, request.form)
        return redirect(url_for('restaurant_menu', restaurant_name=dish['restaurant_name'].replace(" ", "_").lower()))
    return render_template('edit_dish.html', dish=dish)

@app.route('/add_dish/<restaurant_name>', methods=['GET', 'POST'])
def add_dish(restaurant_name):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dishes (name, description, price, image_url, restaurant_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, price, image_url, restaurant_name.replace("_", " ").title()))
        conn.commit()
        conn.close()
        return redirect(url_for('restaurants'))
    return render_template('add_dish.html', restaurant_name=restaurant_name)

@app.route('/delete_dish/<int:dish_id>', methods=['POST'])
def delete_dish(dish_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT restaurant_name FROM dishes WHERE id = ?', (dish_id,))
        dish = cursor.fetchone()
        if dish:
            cursor.execute('DELETE FROM dishes WHERE id = ?', (dish_id,))
            conn.commit()
        return redirect(url_for('restaurant_menu', restaurant_name=dish['restaurant_name'].replace(" ", "_").lower()))
    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect(url_for('restaurant_menu', restaurant_name=dish['restaurant_name'].replace(" ", "_").lower()))
    finally:
        conn.close()

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    conn = get_db_connection()
    if request.method == 'POST':
        restaurant_name = request.form['restaurant_name']
        user_name = session.get('user_name', 'Anonymous')  # נניח שהשם נלקח מהמשתמש המחובר
        rating = request.form['rating']
        comment = request.form['comment']
        
        conn.execute('INSERT INTO recommendations (restaurant_name, user_name, rating, comment) VALUES (?, ?, ?, ?)',
                     (restaurant_name, user_name, rating, comment))
        conn.commit()
    
    recommendations = conn.execute('SELECT * FROM recommendations').fetchall()
    conn.close()
    
    user_role = session.get('user_role', 'guest')  # נניח שסוג המשתמש נשמר ב-session
    return render_template('recommendations.html', recommendations=recommendations, user_role=user_role)

@app.route('/delete_recommendation/<int:id>', methods=['POST'])
def delete_recommendation(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM recommendations WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('recommendations'))

if __name__ == '__main__':
    app.run(debug=True)