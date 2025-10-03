# Shop Management Web Application

**Shop Management Web Application** is a full-stack web application built with FastAPI, providing both a RESTful API and a user-friendly web interface for managing shop items, shopping carts, and users. It uses Supabase for PostgreSQL database hosting and is ready for deployment on Railway Cloudflare.

---

## 🟠 Workflow Status

[![GitHub Actions Status](https://github.com/KhoaNguyen01004/QuanLyBanHang/actions/workflows/python-app.yml/badge.svg)](https://github.com/KhoaNguyen01004/QuanLyBanHang/actions/workflows/python-app.yml)
> **Latest run:** [See latest run details](https://github.com/KhoaNguyen01004/QuanLyBanHang/actions/workflows/python-app.yml) on branch `master`

---

## Features

- **Item Management**: CRUD operations for shop items
- **Cart Management**: Add/remove items from shopping carts
- **User Management**: Basic user registration and authentication (extensible)
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Web Interface**: User-friendly web pages for login, registration, and welcome
- **Database**: PostgreSQL via Supabase
- **Testing**: Comprehensive unit and integration tests

## Repository Structure

```
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic services
│   ├── api/                 # API route handlers
│   ├── db/                  # Database configuration
│   └── core/                # Application configuration
├── static/                  # Static files (CSS, JS, images)
├── templates/               # Jinja2 HTML templates
├── tests/
│   └── test_everything.py   # Unit and integration tests
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (configure for your setup)
├── alembic/                 # Database migrations (optional)
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Supabase account for database
- Railway account for deployment (optional)

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/KhoaNguyen01004/QuanLyBanHang.git
   cd QuanLyBanHang
   ```

2. **Create a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env` and update with your Supabase credentials:
   ```env
   DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@db.[YOUR_PROJECT_REF].supabase.co:5432/postgres
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

### Database Setup

1. Create a new project in [Supabase](https://supabase.com)
2. Get your database URL from the project settings
3. Update the `DATABASE_URL` in `.env`
4. The application will automatically create tables on startup

### Running the Application

**Development:**
```sh
uvicorn app.main:app --reload
```

**Production:**
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation. Access the web interface at `http://localhost:8000`.

### Web Routes

- `GET /` - Login page (redirects to welcome if logged in)
- `GET /welcome` - Welcome page (requires login)
- `GET /logout` - Logout and redirect to login
- `GET /register` - Redirect to user registration API
- `GET /login` - Redirect to user login API

### API Endpoints

#### Items
- `GET /api/items/` - List all items
- `GET /api/items/{item_id}` - Get specific item
- `POST /api/items/` - Create new item
- `PUT /api/items/{item_id}` - Update item
- `DELETE /api/items/{item_id}` - Delete item

#### Carts
- `GET /api/carts/{cart_id}` - Get cart details
- `POST /api/carts/` - Create new cart
- `POST /api/carts/{cart_id}/items` - Add item to cart
- `DELETE /api/carts/{cart_id}/items/{item_id}` - Remove item from cart
- `PUT /api/carts/{cart_id}/items/{item_id}` - Update item quantity

#### Users
- `GET /api/users/{user_id}` - Get user details
- `GET /api/users/email/{email}` - Get user by email
- `POST /api/users/` - Create new user

### Testing

Run the test suite:
```sh
python -m unittest tests/test_everything.py
```

### Deployment to Railway

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `DEBUG=False`
3. Deploy automatically on push

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the [MIT License](LICENSE).

## Authors

- [Khoa Nguyen](https://github.com/KhoaNguyen01004)
- [Thao Nguyen](https://github.com/TyraJr1)

---

## Future Features

More features will be added soon to enhance the functionality and user experience of the Shop Management Web Application.
