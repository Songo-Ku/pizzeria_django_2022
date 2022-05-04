class OrderViewSetTestCase(APITestCase):
    order_detail_uri = '/api/orders/{}/'

    @classmethod
    def setUpClass(cls):
        cls.contact_user1 = ContactUserFactory()
        cls.contact_user2 = ContactUserFactory()

        cls.order_list_url = reverse("order-list")
        cls.user1 = UserFactory()
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        cls.restaurant2 = RestaurantFactory(owner=cls.user1)

        cls.order1 = OrderFactory(restaurant=cls.restaurant1, contact_user=cls.contact_user1)
        # cls.restaurant_list_url = reverse("restaurant-list")
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user1)
        self.amount_order = Order.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    def post_correct_input_order(self):
        valid_order = {
            "restaurant": self.restaurant1.id,
            "contact_user": self.contact_user1.id
        }
        return self.client.post(self.order_list_url, data=valid_order)

    def post_incorrect_input_order(self):
        invalid_restaurant = {"contact_user": "wrong data", "restaurant": "wrong data"}
        return self.client.post(self.order_list_url, data=invalid_restaurant)

    def test_status_add_correct_order(self):
        response = self.post_correct_input_order()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_post_correct_input_order_saved_to_db(self):
        response = self.post_correct_input_order()
        self.assertEquals(Order.objects.count(), self.amount_order + 1)
        self.assertEqual(response.data.get('ordered_products'), [])
        self.assertEqual(Order.objects.get(pk=response.data.get("pk")).restaurant.id, self.restaurant1.id)

    def test_post_incorrect_input_order_do_not_saved_to_db(self):
        response = self.post_incorrect_input_order()
        self.assertEquals(Order.objects.count(), self.amount_order)

    def test_add_incorrect_order_status_400(self):
        response = self.post_incorrect_input_order()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_list_order(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), self.amount_order)
        self.assertEqual(Order.objects.get(id=self.order1.id).restaurant, self.order1.restaurant)

    # tdd assumptions
    def test_get_order_detail(self):
        order_ = OrderFactory(restaurant=self.restaurant2, contact_user=self.contact_user2)
        response = self.client.get(self.order_detail_uri.format(order_.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('contact_user'), self.contact_user2.id)
        self.assertEqual(response.data.get('restaurant'), self.restaurant2.id)
        self.assertEqual(response.data.get('pk'), order_.id)
        self.assertEqual(response['content-type'], 'application/json')

    def test_for_not_existed_order(self):
        response = self.client.get(self.order_detail_uri.format(self.amount_order + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
