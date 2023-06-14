from django.test import TestCase

from .models import ExpSmoothingParams


class ExpSmoothingParamsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ExpSmoothingParams.objects.create(interp_frequency='3h', seasonal_periods=11, forecast_horizon=29)

    def test_interp_frequency_label(self):
        instance = ExpSmoothingParams.objects.get(id=1)
        field_label = instance._meta.get_field('interp_frequency').verbose_name
        self.assertEquals(field_label, 'Дискрета для интерполяции')

    def test_seasonal_periods_label(self):
        instance = ExpSmoothingParams.objects.get(id=1)
        field_label = instance._meta.get_field('seasonal_periods').verbose_name
        self.assertEquals(field_label, 'Сезонность ряда')

    def test_interp_frequency_max_length(self):
        instance = ExpSmoothingParams.objects.get(id=1)
        max_length = instance._meta.get_field('interp_frequency').max_length
        self.assertEquals(max_length, 5)

    def test_object_str(self):
        instance = ExpSmoothingParams.objects.get(id=1)
        expected_object_name = 'Гиперпараметры модели'
        self.assertEquals(expected_object_name, str(instance))


class GraphViewTest(TestCase):

    # @classmethod
    # def setUpTestData(cls):
    #     #Create 13 authors for pagination tests
    #     number_of_authors = 13
    #     for author_num in range(number_of_authors):
    #         Author.objects.create(first_name='Christian %s' % author_num, last_name = 'Surname %s' % author_num,)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/req/graph/')
        self.assertEqual(resp.status_code, 200)
