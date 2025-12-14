# 🛍️ Stellaric Apparel Co. - E-commerce Platform

A modern, full-stack e-commerce application built with Django and Alpine.js, featuring a clean UI, shopping cart functionality, user authentication, and order management.

![Django]
![Python]
![Bootstrap]
![Alpine.js]

## ✨ Features

### 🛒 Shopping & Products
- **Product Catalog**: Browse products with images, descriptions, and pricing
- **Product Details**: View detailed product information with size selection
- **Shopping Cart**: Add, remove, and update product quantities
- **Dynamic Pricing**: Real-time cart total calculation with discount support
- **Size Selection**: Choose from multiple size options (PP, P, M, G, GG)

### 👤 User Management
- **User Registration**: Create new accounts with email verification
- **Authentication**: Secure login/logout functionality
- **User Profiles**: Manage personal information and addresses
- **Inline Profile Edit**: Edit profile details with Alpine.js-powered UI
- **Purchase History**: Track order status and past purchases

### 💰 Shopping Experience
- **Coupon System**: Apply discount codes (e.g., STELLA15 for 15% off)
- **Order Tracking**: View shipping status with tracking codes
- **Responsive Design**: Mobile-friendly interface
- **Toast Notifications**: Real-time feedback for user actions

### 🎨 UI/UX
- **Modern Interface**: Clean, professional design
- **Smooth Animations**: Hover effects and transitions
- **Alpine.js Components**: Interactive elements without page reloads
- **Bootstrap Styling**: Consistent, responsive layout

## 🛠️ Tech Stack

### Backend
- **Django 5.2.8**: High-level Python web framework
- **SQLite**: Lightweight database for development
- **Pillow**: Image processing library for product photos
- **Python 3.13**: Programming language

### Frontend
- **HTML5 & CSS3**: Modern web standards
- **JavaScript (ES6+)**: Interactive functionality
- **Bootstrap 5.3.2**: CSS framework for responsive design
- **Alpine.js 3.x**: Lightweight JavaScript framework
- **Font Awesome**: Icon library

### Deployment
- **Railway**: Cloud platform for deployment
- **Gunicorn**: WSGI HTTP server
- **WhiteNoise**: Static file serving

## 📥 Installation

### Prerequisites
- Python 3.13 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/stellaric-ecommerce.git
cd stellaric-ecommerce
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup database**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Frontend: `http://127.0.0.1:8000/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Settings Overview

Key settings in `djangoProject/settings.py`:
```python
# Security
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['fullstack-django-project-production.up.railway.app', 'localhost']

# Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
```

## 📖 Usage

### Adding Products (Admin)

1. Navigate to `/admin/`
2. Login with superuser credentials
3. Click on "Products" → "Add Product"
4. Fill in product details:
   - Name
   - Price
   - Description
   - Stock quantity
   - Upload image

### Shopping Flow (Customer)

1. **Browse Products**: Visit `/shop/` to see all products
2. **View Details**: Click on a product to see full details
3. **Add to Cart**: Select size and click "Add to Cart"
4. **Manage Cart**: Visit `/cart/` to update quantities or remove items
5. **Apply Coupon**: Enter `STELLA15` for 15% discount
6. **Checkout**: Click "Proceed to Checkout"

### User Profile Management

1. **Register**: Create account at `/auth/register/`
2. **Login**: Access account at `/auth/login/`
3. **Edit Profile**: Visit `/userSection/` and click "Edit"
4. **Update Info**: Modify address, phone, city, state, zipcode
5. **View Orders**: Check purchase history in user section

## 📂 Project Structure
```
stellaric-ecommerce/
│
├── djangoProject/          # Main project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI entry point
│
├── stellaric/             # Main app
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template
│   │   ├── index.html     # Homepage
│   │   ├── shop.html      # Product listing
│   │   └── product.html   # Product details
│   ├── views.py           # View functions
│   └── static/            # Static files
│
├── users/                 # User management app
│   ├── models.py          # User Profile model
│   ├── views.py           # Auth views
│   ├── urls.py            # User URLs
│   └── templates/         # User templates
│       ├── login.html
│       ├── user.html      # Registration
│       └── userSection.html
│
├── cart/                  # Shopping cart app
│   ├── models.py          # Cart, CartItem, Product models
│   ├── views.py           # Cart operations
│   ├── urls.py            # Cart URLs
│   └── templates/
│       └── cart.html
│
├── assets/                # Static assets
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── img/
│
├── media/                 # Uploaded files
│   └── products/          # Product images
│
├── staticfiles/           # Collected static files
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment
├── db.sqlite3            # SQLite database
└── README.md             # This file
```

## 🔗 API Endpoints

### Public Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage |
| GET | `/shop/` | Product listing |
| GET | `/about/` | About page |
| GET | `/product/<id>/` | Product details |

### Authentication Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/auth/register/` | User registration |
| GET/POST | `/auth/login/` | User login |
| GET | `/auth/logout/` | User logout |

### User Routes (Protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/userSection/` | User profile |
| POST | `/auth/update-profile/` | Update profile |

### Cart Routes (Protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cart/` | View cart |
| POST | `/cart/add/<product_id>/` | Add to cart |
| POST | `/cart/remove/<item_id>/` | Remove from cart |
| POST | `/cart/update/<item_id>/` | Update quantity |
| POST | `/cart/coupon/` | Apply coupon |

## 📸 Screenshots

### Homepage
<img width="1920" height="938" alt="image" src="https://github.com/user-attachments/assets/4e64b29a-483b-4f67-81c0-b667763f7113" />

### Login 
<img width="1920" height="933" alt="image" src="https://github.com/user-attachments/assets/e70454d6-acea-4b6f-a07b-90a87e904ac8" />

### User Profile
<img width="1920" height="940" alt="image" src="https://github.com/user-attachments/assets/8ce102f0-2330-42da-a146-c234213c88a7" />



**Live Demo**: [https://fullstack-django-project-production.up.railway.app](https://fullstack-django-project-production.up.railway.app)
