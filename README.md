# Shop Management Web Application

A FastAPI web app for browsing items, managing a cart, and placing orders with a simple web UI. It exposes REST APIs, serves HTML templates, persists data (SQLite by default), and is deployable on Railway. Sessions are used for web auth; JWT is available for API token flows.

**Key features**
- Items: browse and CRUD via API
- Cart: guest or user cart, quantity updates, stock tracking
- Orders: checkout creates an order from cart and clears it
- WebSockets: stock updates broadcast to connected clients
- Auth: register/login via session; optional OAuth2 password/token endpoint
- New: Print Receipt on checkout confirmation page

**Tech stack**
- FastAPI, Starlette Sessions, SQLAlchemy, Pydantic
- Jinja2 templates, vanilla JS frontend
- SQLite by default (DATABASE_URL configurable to Postgres, e.g. Supabase)

**Repository layout** (trimmed)
- app/
  - main.py (FastAPI app, middleware, routes mounting)
  - api/ (users, carts, items, orders)
  - services/ (shop_services business logic)
  - models/ (SQLAlchemy models)
  - schemas/ (Pydantic schemas)
  - core/ (config, security)
  - db/ (engine/session)
- templates/ (home, cart, checkout, purchases, login, register)
- static/ (css, images)
- scripts/ (populate_items.py)
- Diagrams/ (PlantUML activity + state diagrams)
- tests/ (pytest test suite)

---

## Quickstart

### 1) Prerequisites
- Python 3.10+

### 2) Create and activate a virtualenv
- Windows (cmd.exe):
```bat
python -m venv .venv
.venv\Scripts\activate
```
- PowerShell:
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```
- Linux/macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Environment variables
Create a `.env` at project root (or set these in your environment):
```env
# Required
SECRET_KEY=change-me

# Optional (SQLite used if not set)
DATABASE_URL=sqlite:///./test.db

# Dev convenience
DEBUG=true
INSECURE_SESSIONS=1         # use insecure cookies locally (http)
COOKIE_SAMESITE=lax         # cookie SameSite (lax|none|strict)

# CORS: must be explicit when sending credentials (cookies)
ALLOWED_ORIGINS=http://localhost:8000

# JWT (token login API)
JWT_SECRET_KEY=test-secret-key-for-development
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```
**Notes**
- When `allow_credentials` is true (default here), browsers refuse `"*"` for CORS. Set `ALLOWED_ORIGINS` to a comma-separated list of exact origins, e.g.:
  - `ALLOWED_ORIGINS=https://your-app.up.railway.app,http://localhost:8000`
- `INSECURE_SESSIONS=1` for local HTTP only. In production keep it off; cookies will be https-only.

### 5) Run locally
Use the ASGI app to ensure session middleware is active:
```bash
uvicorn app.main:asgi_app --reload --host 127.0.0.1 --port 8000
```
Open [http://localhost:8000](http://localhost:8000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Home UI: home page with items
- Cart and Checkout available from the UI

### Populate demo items (optional)
- Windows (cmd.exe):
```bat
set SECRET_KEY=dev-secret
python -m scripts.populate_items
```
- PowerShell:
```powershell
$env:SECRET_KEY='dev-secret'
python -m scripts.populate_items
```
- Linux/macOS:
```bash
SECRET_KEY=dev-secret python -m scripts.populate_items
```
Defaults to SQLite `test.db`. To target another DB, set `DATABASE_URL` before the command.

### Testing
Run the pytest test suite from project root:
```bash
pytest -q
```

### Deployment (Railway)
- Start command: the included Procfile uses
  - `web: python app/main.py`
  which runs uvicorn with the correct app (`asgi_app`) inside `main.py`.
- Set environment variables in your Railway service:
  - `SECRET_KEY`: a strong secret
  - `DATABASE_URL`: e.g., Postgres connection (optional if staying on SQLite)
  - `DEBUG`: false
  - `ALLOWED_ORIGINS`: https://your-app.up.railway.app (plus any allowed localhost origins)
  - `COOKIE_SAMESITE`: lax (or none with https)
  - `INSECURE_SESSIONS`: 0
  - `JWT_*` if you plan to use token auth endpoints
- CORS with cookies: Do not use `"*"` in `ALLOWED_ORIGINS` when `allow_credentials=true`. Use exact origins.

---

## Routes overview
- **Web**
  - `GET /`                Home (renders items; shows user if logged in)
  - `GET /cart`            Cart page (guest carts supported via session_id)
  - `GET /checkout`        Checkout page (prints receipt after success)
  - `GET /purchases`       Past orders (after login)
  - `GET /login`           Redirects to /api/users/login (form)
  - `GET /register`        Redirects to /api/users/register (form)
  - `GET /logout`          Clears session and redirects home
  - `GET /health`          Health check
  - `WS /ws/stock-updates` Broadcast stock updates
- **API** (selection)
  - Items:    `GET /api/items`, `GET/PUT/DELETE /api/items/{id}`, `POST /api/items`
  - Carts:    `POST /api/carts` (ensure/create), `GET /api/carts/{id}`
               `POST /api/carts/{id}/items` (add), `PUT /api/carts/{id}/items/{item_id}` (qty),
               `DELETE /api/carts/{id}/items/{item_id}`
  - Orders:   `POST /api/orders/checkout` (create order from current cart), `GET /api/orders/my`
  - Users:    `GET /api/users/{user_id}`, `POST /api/users` (register), `POST /api/users/token` (JWT)

### New: Print Receipt
- After a successful checkout on `/checkout`, the page renders a receipt and exposes a "Print Receipt" button.
- The print function opens a new print-friendly window and invokes the browser print dialog.
- Source: `templates/checkout.html` (`printReceipt` and `buildReceiptHTML` functions).

---

## Diagrams
- PlantUML activity and state diagrams live in `Diagrams/Activity.puml` and `Diagrams/State.puml`.
- Updated to include the Print Receipt flow (confirmation → print). 

---

## Troubleshooting
- **401/Not authenticated on cart actions**:
  - Run via `app.main:asgi_app` so SessionMiddleware applies.
  - Ensure you’re logged in via the web UI; fetch calls must use `credentials: 'include'`.
- **CORS/cookies not sent on Railway**:
  - Set `ALLOWED_ORIGINS` to your exact Railway origin (no `"*"`).
  - Keep `COOKIE_SAMESITE=lax` (or none with full https) and don’t set `INSECURE_SESSIONS` in production.
- **307 redirects in Railway logs**:
  - Railway/Cloudflare enforce HTTPS at the edge; the app supports it. Ensure browser uses https URL.

---

## License
- MIT License (see LICENSE)
