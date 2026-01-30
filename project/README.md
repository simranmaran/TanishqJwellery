# Tanishq Jewellery E-commerce Website

A fully functional e-commerce website for Tanishq Jewellery built with Django.

## Features

- User authentication and registration
- Product browsing with categories, filters, and search
- Shopping cart with session management
- Wishlist functionality
- Order placement and tracking
- Admin panel for managing products, categories, orders, and users
- Responsive design with Bootstrap 5

## Setup Instructions

1. **Clone or download the project** to your local machine.

2. **Navigate to the project directory**:
   ```
   cd project
   ```

3. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies** (if requirements.txt exists, otherwise Django is included):
   ```
   pip install django
   ```

5. **Run migrations**:
   ```
   python manage.py migrate
   ```

6. **Create a superuser for admin access**:
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

7. **Run the development server**:
   ```
   python manage.py runserver
   ```

8. **Access the website**:
   - Main site: http://127.0.0.1:8000/
   - Admin login: http://127.0.0.1:8000/dashboard/admin-login/

## Usage

- **Customer Features**:
  - Register/Login as a customer
  - Browse products, use filters and search
  - Add products to cart and wishlist
  - Place orders
  - View order history

- **Admin Features**:
  - Login with superuser credentials
  - Manage products (add, edit, delete)
  - Manage categories
  - View and update order statuses
  - Manage users (block/unblock)

## Sample Data

To add sample data, you can use the admin panel or create a management command. For now, manually add categories and products through the admin interface.

## Technologies Used

- Python 3.x
- Django 5.x
- Bootstrap 5
- SQLite (default database)

## Notes

- Image URLs are placeholders; replace with actual Cloudinary URLs for production.
- This is a demo setup; for production, configure proper settings, database, and security measures.