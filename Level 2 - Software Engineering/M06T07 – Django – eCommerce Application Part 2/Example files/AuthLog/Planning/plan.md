# eCommerce Project — Planning

## Overview
Small eCommerce web app with two main user roles: Vendors and Buyers. Vendors create and manage Stores and Products. Buyers browse the product catalog, add products to cart, checkout, and leave reviews. Admin/superusers can manage stores and products from the Django admin and the main app.

## Requirements
- Users: `Vendor`, `Buyer`, `Admin` (Django superuser).
- Vendors: create/view/edit/delete Stores; manage Products within their Stores.
- Buyers: browse products across Stores, add to cart (session-backed), checkout, receive invoice by email.
- Reviews: verified if buyer purchased the product; otherwise unverified.
- Authentication, password reset via timed email tokens.

## Models (high-level)
- `Store` (owner -> User, name, description, created_at)
- `Product` (store -> Store, name, description, price, stock, vendor optional)
- `Order`, `OrderItem` (cart -> Order on checkout)
- `Review` (product, user, rating, comment, verified)

## UI Layout (pages)
- Welcome/login page
- Product catalog page at `/ecommerce/`
- Product detail page (add to cart, reviews)
- Cart page (session-backed)
- Checkout + success page (invoice email)
- Vendor store dashboard at `/ecommerce/stores/` (create/edit/delete stores)
- Product creation page for vendors to add products to a chosen store
- Auth pages: register, login, password reset request/confirm

## Access Control & Security
- Use Django auth with groups to distinguish Vendors and Buyers.
- Permissions: vendors/superusers can manage their stores and products; buyers can browse, add to cart, checkout, and review products.
- Use `login_required` and per-view checks; enforce in templates and views.
- Password reset uses expiring tokens and email delivery.
- Use HTTPS in production; keep `SECRET_KEY` out of VCS; use environment variables for DB and email credentials.

## Database & Migrations
- Target DB: MariaDB (or MySQL). Update `DATABASES` in `AuthLog/settings.py` and install `mysqlclient` or `PyMySQL` adapter.
- Run `makemigrations` and `migrate` after model changes.

## Failure Modes & Recovery
- Stock race: wrap checkout in DB transaction; validate stock before creating OrderItems.
- Email send failure: mark `email_sent=False`, retryable background job or admin-visible queue.
- Partial failures: use atomic transactions to rollback on error.
- Data validation: validate user input in forms and models.

## Next small step (recommended)
1. Add `Store` model and migrate `Product` to belong to `Store` (update relationships and migrations).
2. Implement Store CRUD views and templates.

## Part 2 – REST API Planning
A separate planning note has been added in `Planning/api_plan.md` for the API extension work.

It covers:
- the API goal and scope
- the main resources to expose
- suggested endpoints for stores, products, and reviews
- authentication and permission expectations

The next planned step is to turn this into a sequence diagram before implementation begins.

Placeholders and notes:
- Keep planning concise; expand diagrams/screenshots locally if desired.
