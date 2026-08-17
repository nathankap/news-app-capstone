import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from .models import Product, Review, Store


class EcommerceRequirementsTests(TestCase):
    """Verify the M06T07 store, product, and review requirements."""

    def setUp(self):
        user_model = get_user_model()
        self.vendor = user_model.objects.create_user(
            username='vendor', password='secret')
        self.other_vendor = user_model.objects.create_user(
            username='other-vendor', password='secret')
        self.buyer = user_model.objects.create_user(
            username='buyer', password='secret')
        Group.objects.get_or_create(name='Vendors')[0].user_set.add(
            self.vendor, self.other_vendor)
        Group.objects.get_or_create(name='Buyers')[0].user_set.add(
            self.buyer)
        self.store = Store.objects.create(
            owner=self.vendor,
            name='Main Store',
            description='Primary store',
        )
        self.product = Product.objects.create(
            vendor=self.vendor,
            store=self.store,
            name='Widget',
            description='Useful widget',
            price='10.00',
            stock=5,
        )

    def test_users_can_follow_vendor_store_and_product_paths(self):
        """The three public catalog entry points are reachable."""
        for url in (
            '/ecommerce/vendors/',
            '/ecommerce/stores/',
            '/ecommerce/',
            f'/ecommerce/vendors/{self.vendor.id}/stores/',
            f'/ecommerce/stores/{self.store.id}/products/',
        ):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)

    def test_vendor_can_retrieve_reviews_as_a_list(self):
        """Vendors can see reviews with their product and store context."""
        Review.objects.create(
            product=self.product,
            user=self.buyer,
            rating=4,
            comment='Good product',
        )
        self.client.force_login(self.vendor)
        response = self.client.get('/ecommerce/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Widget')
        self.assertContains(response, 'Main Store')

    def test_api_supports_all_retrieval_entry_points(self):
        """JSON retrieval covers vendors, stores, products, and reviews."""
        urls = (
            '/ecommerce/api/vendors/',
            f'/ecommerce/api/vendors/{self.vendor.id}/stores/',
            '/ecommerce/api/stores/',
            f'/ecommerce/api/stores/{self.store.id}/products/',
            '/ecommerce/api/products/',
            f'/ecommerce/api/products/{self.product.id}/reviews/',
        )
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)
            self.assertIn('application/json', response['Content-Type'])

    def test_vendor_can_create_store_and_product_through_api(self):
        """Only the vendor can create the API-owned resources."""
        self.client.force_login(self.vendor)
        store_response = self.client.post(
            '/ecommerce/api/stores/',
            data=json.dumps({'name': 'Second Store'}),
            content_type='application/json',
        )
        self.assertEqual(store_response.status_code, 201)
        new_store_id = store_response.json()['id']
        product_response = self.client.post(
            f'/ecommerce/api/stores/{new_store_id}/products/',
            data=json.dumps({
                'name': 'Second Product',
                'price': '12.50',
                'stock': 3,
            }),
            content_type='application/json',
        )
        self.assertEqual(product_response.status_code, 201)

    def test_vendor_add_product_page_requires_store_selection(self):
        """The add-product form must capture which store owns the product."""
        self.client.force_login(self.vendor)

        response = self.client.get('/ecommerce/product/add/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="store_id"')

        response = self.client.post(
            '/ecommerce/product/add/',
            {
                'name': 'Selected Product',
                'description': 'Chosen store',
                'price': '8.99',
                'stock': 2,
                'store_id': self.store.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Product.objects.filter(
                name='Selected Product',
                store=self.store,
                vendor=self.vendor,
            ).exists()
        )

    def test_other_vendor_cannot_add_to_store(self):
        """A vendor cannot create products in another vendor's store."""
        self.client.force_login(self.other_vendor)
        response = self.client.post(
            f'/ecommerce/api/stores/{self.store.id}/products/',
            data=json.dumps({
                'name': 'Blocked',
                'price': '2.00',
                'stock': 1,
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)