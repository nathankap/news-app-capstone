# M06T07 Part 2 API Plan

## Read endpoints

- `GET /ecommerce/api/vendors/`
- `GET /ecommerce/api/vendors/<vendor_id>/stores/`
- `GET /ecommerce/api/stores/`
- `GET /ecommerce/api/stores/<store_id>/products/`
- `GET /ecommerce/api/products/`
- `GET /ecommerce/api/products/<product_id>/reviews/`
- `GET /ecommerce/api/vendors/reviews/` for the authenticated vendor

These endpoints support vendor-to-store, store-to-product, and direct product
retrieval. Review responses include product and user context.

## Write endpoints

- `POST /ecommerce/api/stores/` creates a store for the authenticated vendor.
- `POST /ecommerce/api/stores/<store_id>/products/` creates a product only
  for that store's vendor.

## Access control

Read operations are public. Creation requires an authenticated vendor, and a
vendor may only add products to that vendor's own store.
