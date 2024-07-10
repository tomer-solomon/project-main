
# Food Ordering Website

## Project Overview

This project was developed as a final project for the second year of studies in Information Systems Management and Business Management. The project follows a structured outline provided by the course instructor and focuses on the creation of a food ordering website.

## Objective

The primary objective of this project is to design and implement an efficient and user-friendly food ordering system. The project began with a meticulous planning phase, identifying the essential pages to be displayed and determining how to connect them effectively. The project emphasizes the use of template inheritance (`extends`) to implement the design efficiently.

## Features

1. **User Authentication**: 
   - Registration and login functionality for users.
   - Secure password handling and user session management.

2. **Food Menu**: 
   - Display a comprehensive menu of available food items.
   - Options to add items to the cart.

3. **Order Management**: 
   - Users can place orders and view their order history.
   - Admin can manage orders and update order status.

4. **Database Integration**:
   - Use of SQLite for database management.
   - Tables are created using SQL commands within the code.
   - Relational database design for ease of use and efficiency.

## User Types and Responsibilities

### Regular Users
- **Registration and Login**: Users can create an account and log in to access the system.
- **View Menu**: Users can browse the available food items.
- **Order Food**: Users can add items to their cart and place orders.
- **View Order History**: Users can view their past orders and current order status.

### Admin Users
- **Manage Orders**: Admin users can view, update, and manage all orders placed by users.
- **Update Menu**: Admins have the ability to add, edit, or remove items from the menu.
- **User Management**: Admins can manage user accounts, including activating or deactivating accounts.

### Operator Users
- **Order Processing**: Operators can view and process incoming orders.
- **Update Order Status**: Operators can update the status of orders (e.g., preparing, ready for pickup, delivered).
- **Delete Recommendations**: Operators can delete recommendations on the recommendations page.

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite
- **Template Engine**: Jinja2

## Project Structure

- **static/**: Contains static files such as CSS, JavaScript, and images.
- **templates/**: Contains HTML templates for rendering the web pages.
- **venv/**: Virtual environment directory containing dependencies.
- **app.py**: The main application script that initializes and runs the Flask app.
- **users.db**: SQLite database file.

## Implementation Details

1. **Planning and Design**:
   - The project started with a detailed planning phase, where the pages and their connections were carefully designed.
   - The efficiency and usability were key considerations, leading to the use of template inheritance (`extends`) for consistent and maintainable design.

2. **Database Choice**:
   - SQLite was chosen for its simplicity and ease of integration.
   - The database schema was designed to be relational, allowing for efficient data management.
   - Tables were created using SQL commands directly in the code for dynamic and flexible database handling.

## Getting Started

To get a local copy up and running, follow these steps:

### Prerequisites

- Python 3.7+
- Flask

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/tomer-solomon/project.git
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python app.py
   ```

## Usage

- Navigate to `http://localhost:5000` in your web browser to use the application.
- Register or log in to access the food menu and place orders.
- Admin users can manage orders through the admin panel.

## Contribution

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code follows the project's coding standards and includes appropriate tests.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

For any inquiries or issues, please open an issue on the GitHub repository or contact the project maintainer.


### Screens
here is a link to view the project screens: https://drive.google.com/drive/folders/1NEFc-DIFQfb9WvDR0cMnsiBtk5DUSz_V?usp=sharing