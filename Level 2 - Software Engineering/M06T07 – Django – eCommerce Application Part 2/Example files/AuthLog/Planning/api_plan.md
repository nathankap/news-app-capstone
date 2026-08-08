# eCommerce Project — Part 2 Planning: REST API

## Goal
Extend the existing Django eCommerce project with a RESTful API so that vendors can manage stores and products, and both buyers and vendors can retrieve store and product information.

## Scope
- Vendors can create new stores through the API.
- Vendors can add products to their own stores through the API.
- Vendors can retrieve reviews for their products or stores.
- Buyers and vendors can retrieve the stores belonging to a vendor and the products belonging to a store.
- Authentication is required before any resource-changing action.

## Proposed API Style
- Use Django REST Framework.
- Use JSON as the primary response format.
- Keep the API simple, predictable, and aligned with the existing Django models.

## Suggested Resources and Serialisation
- Store resource: `id`, `name`, `description`, `owner`, `created_at`
- Product resource: `id`, `store`, `name`, `description`, `price`, `stock`
- Review resource: `id`, `product`, `user`, `rating`, `comment`, `verified`

## Suggested Endpoints
- `GET /api/stores/` — list all stores
- `POST /api/stores/` — create a new store (vendor only)
- `GET /api/vendors/<vendor_id>/stores/` — list stores for a specific vendor
- `GET /api/stores/<store_id>/products/` — list products for a specific store
- `POST /api/stores/<store_id>/products/` — add a product to a store (vendor only)
- `GET /api/products/<product_id>/reviews/` — retrieve reviews for a product

## Authentication and Permissions
- Use token-based or session-based authentication.
- Only vendors or superusers should be allowed to create or edit stores and products.
- Buyers and vendors should be able to read store and product data.
- Review retrieval should be restricted to relevant users where appropriate.

## Notes for Later Implementation
- The API should remain focused on the required task features and avoid adding unnecessary functionality.
- The next step will be to turn this plan into a sequence diagram before implementation begins.
