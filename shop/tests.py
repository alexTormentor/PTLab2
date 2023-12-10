from django.test import TestCase
from django.urls import reverse
from .models import Product, Purchase

class ShopTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100, alcohol_type="Test Type", quantity=10)
        self.purchase_data = {'person': 'John Doe', 'address': '123 Main St.'}

    def test_index_view_add_to_cart(self):
        response = self.client.post(reverse('index'), {'product_id': self.product.id})
        self.assertEqual(response.status_code, 302)

        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.quantity, self.product.quantity + 1)


    def test_purchase_create_view(self):
        response = self.client.post(reverse('buy', args=[self.product.id]), self.purchase_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.person, self.purchase_data['person'])
        self.assertEqual(purchase.address, self.purchase_data['address'])


    def test_cart_view(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('cart_items', response.context)
        self.assertIn('total_items', response.context)
        self.assertEqual(response.context['total_items'], self.product.quantity)
        self.assertEqual(len(response.context['cart_items']), 1)


    def test_edit_cart_view_remove_item(self):
        response = self.client.post(reverse('edit_cart'), {'product_id': self.product.id, 'action': 'remove'})
        self.assertEqual(response.status_code, 200)

        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.quantity, 0)


    def test_edit_cart_view_decrease_item(self):
        response = self.client.post(reverse('edit_cart'), {'product_id': self.product.id, 'action': 'decrease'})
        self.assertEqual(response.status_code, 200)

        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.quantity, self.product.quantity - 1)


    def test_purchase_success_view(self):
        purchase = Purchase.objects.create(product=self.product, person='John Doe', address='123 Main St.')
        response = self.client.get(reverse('purchase_success'),
                                   {'product_id': self.product.id, 'person': 'John Doe', 'address': '123 Main St.'})
        self.assertEqual(response.status_code, 200)

        self.assertIn('product', response.context)
        self.assertIn('person', response.context)
        self.assertIn('address', response.context)
        self.assertEqual(response.context['product'], purchase.product)
        self.assertEqual(response.context['person'], purchase.person)
        self.assertEqual(response.context['address'], purchase.address)