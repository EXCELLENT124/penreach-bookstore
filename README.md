# Online Bookstore

A complete online bookstore application built with Django, featuring user authentication, shopping cart functionality, order management, and an admin dashboard.

## Features

### Customer Features
- **User Registration & Login**: Customers can create accounts with full name, contact details, and address
- **Book Browsing**: View available books with search functionality
- **Shopping Cart**: Add books to cart, update quantities, remove items
- **Order Placement**: Submit orders without online payment (order submission system)
- **Order History**: View past orders and their status
- **Responsive Design**: Modern, mobile-friendly interface using Tailwind CSS

### Admin Features
- **Book Management**: Add, edit, delete books and set prices in South African Rands
- **Order Management**: View and manage customer orders with status tracking
- **Admin Dashboard**: Comprehensive overview with statistics and analytics
- **Inventory Tracking**: Monitor stock levels and low-stock alerts
- **Sales Analytics**: View top-selling books and revenue reports

## Technology Stack

- **Backend**: Django 6.0.3
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite (development)
- **Image Processing**: Pillow
- **Authentication**: Django's built-in authentication system

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions

1. **Clone or download the project** to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd pbookstore
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser account** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account

6. **Load sample books** (optional):
   ```bash
   python manage.py load_sample_books
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - **Storefront**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/
   - **Admin Dashboard**: http://127.0.0.1:8000/admin-dashboard/

## Usage

### For Customers
1. **Browse Books**: Visit the homepage to see featured books or browse all books
2. **Search**: Use the search bar to find books by title, author, or description
3. **Register**: Create an account with your details
4. **Add to Cart**: Click "Add to Cart" on books you want to purchase
5. **Checkout**: Review your cart and submit your order
6. **Track Orders**: View your order history and status

### For Administrators
1. **Access Admin Panel**: Go to `/admin/` and login with your superuser credentials
2. **Manage Books**: Add new books, update prices, manage inventory
3. **View Orders**: Monitor and update order statuses
4. **Dashboard**: Visit `/admin-dashboard/` for analytics and overview

## Project Structure

```
pbookstore/
├── accounts/          # User authentication and profiles
├── admin_dashboard/   # Custom admin dashboard
├── books/            # Book models and views
├── cart/             # Shopping cart functionality
├── orders/           # Order management
├── bookstore/        # Django project settings
├── static/           # Static files (CSS, JS)
├── media/            # User uploaded files
└── templates/        # HTML templates
```

## Key Features Explained

### Authentication System
- Custom user model with additional fields (full name, phone, address)
- Registration form with validation
- Login/logout functionality
- User profile management

### Shopping Cart
- Session-based cart for guest users
- Persistent cart for logged-in users
- Real-time cart updates
- Quantity management

### Order System
- Order submission without payment
- Order tracking with status updates
- Email confirmation ready (can be extended)
- Order history for customers

### Admin Dashboard
- Real-time statistics
- Sales analytics
- Inventory management
- Low stock alerts
- Top-selling books report

## Customization

### Adding New Fields
To add new fields to the user model or other models:
1. Update the model in the respective app
2. Create and run migrations
3. Update forms and templates accordingly

### Styling
The application uses Tailwind CSS for styling. You can customize:
- Colors and themes in the templates
- Layout and responsive behavior
- Component designs

### Payment Integration
To add payment processing:
1. Install payment gateway package (e.g., Stripe, PayPal)
2. Update the checkout process
3. Add payment forms and validation
4. Handle payment webhooks

## Deployment

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Configure static files serving
5. Set up environment variables for sensitive data
6. Configure a web server (Nginx) and WSGI server (Gunicorn)

## Support

This project includes:
- Comprehensive error handling
- Input validation
- Security best practices
- Responsive design
- Accessibility considerations

## License

This project is for educational purposes. Feel free to modify and use it as needed.

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
