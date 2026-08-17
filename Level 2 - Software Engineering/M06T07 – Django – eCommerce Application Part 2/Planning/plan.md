# M06T07 Part 2 Planning

## Goal

Extend the Django eCommerce application with store and product retrieval
paths, vendor review retrieval, and complete vendor CRUD workflows.

## Requirements and implementation

- Vendors create, view, edit, and delete stores.
- Vendors create, view, edit, and delete products assigned to their stores.
- Vendors retrieve one list of reviews with product and store context.
- Buyers submit product reviews.
- Buyers and vendors browse from vendors to stores to products.
- Buyers and vendors browse directly from stores to products.
- Buyers and vendors browse directly from the complete product list.
- JSON endpoints provide the same retrieval paths.
- Only authenticated vendors can create stores or products through the API.

## Project structure

The project files are in the M06T07 folder beside the Part 2 task PDF.
Old Part 1 research and example snippets are not part of this submission.

## Verification

The test suite covers public navigation, vendor review retrieval, API
retrieval, API creation, and store ownership checks.
