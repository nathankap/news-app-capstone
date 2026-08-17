# Django eCommerce Application - Part 2

This folder contains the complete M06T07 Part 2 Django project. The project files are in the same folder as the Part 2 task PDF.

## Part 2 scope

- Vendors can create, view, edit, and delete stores.
- Vendors can create, view, edit, and delete products.
- Vendors can retrieve one list of reviews for their products.
- Buyers can review products.
- Buyers and vendors can browse through vendors, stores, or products.
- The same retrieval paths are available through JSON endpoints.

## Run the project

Open PowerShell in this folder, then run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

The project uses SQLite when no database variables are set. For MariaDB, install the dependencies above and set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` before running migrations.

## Browser review flow

1. Register a vendor and a buyer from the website.
2. Log in as the vendor and open `eCommerce`.
3. Open `Manage Stores`, then create a store.
4. Open `Add Product`, choose the store, and create a product.
5. Use `Vendors` to open the vendor, then the vendor's stores, then the store's products.
6. Use `Stores` to start directly from all stores and open their products.
7. Use `All Products` to start directly from the product list.
8. Log in as the buyer, open a product, and submit a review.
9. Log back in as the vendor and open `My Reviews` to see one list containing the review and its product/store context.

## Vendor CRUD

The vendor can use the website to:

- Create, edit, view, and delete stores.
- Create products and assign them to one of the vendor's stores.
- Edit and delete products owned by the vendor or the vendor's stores.
- Retrieve all reviews for products owned by the vendor.

## JSON retrieval and creation endpoints

Public read endpoints:

- `GET /ecommerce/api/vendors/`
- `GET /ecommerce/api/vendors/<vendor_id>/stores/`
- `GET /ecommerce/api/stores/`
- `GET /ecommerce/api/stores/<store_id>/products/`
- `GET /ecommerce/api/products/`
- `GET /ecommerce/api/products/<product_id>/reviews/`

Vendor-only endpoints:

- `POST /ecommerce/api/stores/`
- `POST /ecommerce/api/stores/<store_id>/products/`
- `GET /ecommerce/api/vendors/reviews/`

## Tests and checks

```powershell
python manage.py test eCommerce
python manage.py check
```

## Project boundary

The submitted project files are located here beside the task PDF:

```text
manage.py
AuthLog/
eCommerce/
grabsomore/
functions/
Planning/
requirements.txt
README.md
```

`Planning/sequence_vendor.md` and `Planning/sequence_buyer.md` document the complete CRUD, review, and retrieval sequences.
