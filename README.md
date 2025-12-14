Django E-Commerce App 
	•	Developed a full e-commerce backend with product listings, user authentication, session-based cart/checkout flow, and dynamic quantity updates using Django ORM.
	•	Built secure REST APIs with Django REST Framework and implemented Token Authentication for protected operations.
	•	Integrated dummy Stripe workflow for payment processing and structured the project for scalable deployment.

Features
	•	User Authentication: Login, logout, and registration.
	•	Product Browsing: View products with images, prices, and categories.
	•	Product Search: Search products by name or category.
	•	Sorting: Sort products by price, popularity, or rating.
	•	Cart Management: Add/remove products from the cart and view total price.
	•	Checkout: Simulate payments using Stripe test keys.
	•	Admin Dashboard: Manage products, categories, and orders.
	•	Responsive Design: Works on desktop and mobile devices.

  Technologies Used
	•	Backend: Python, Django, Django REST Framework
	•	Database: PostgreSQL (or SQLite for testing)
	•	Frontend: HTML, CSS, JS, Bootstrap
	•	Payment Gateway: Stripe (test mode)
	•	Version Control: Git & GitHub

  Prerequisites
	•	Python 3.x
	•	Django 4.x
	•	PostgreSQL (optional, SQLite for local testing)
	•	Git

  Usage
	•	Open browser at http://127.0.0.1:8000/
	•	Admin panel at http://127.0.0.1:8000/admin/
	•	Browse products, manage cart, and test Stripe payments

  Django-e-commerce-project/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/               # Main Django app (models, views, urls)
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── media/              # Uploaded product images
└── .env                #Environment variables

