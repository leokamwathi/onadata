from test_base import TestBase
from onadata.apps.main.models.meta_data import MetaData, unique_type_for_form


class TestMetaData(TestBase):

    def setUp(self):
        TestBase.setUp(self)
        self._create_user_and_login()
        self._publish_transportation_form_and_submit_instance()

    def test_create_metadata(self):
        count = len(MetaData.objects.filter(object_id=self.xform.id,
                    data_type='enketo_url'))
        enketo_url = "https://dmfrm.enketo.org/webform"
        MetaData.enketo_url(self.xform, enketo_url)
        self.assertEquals(count + 1, len(MetaData.objects.filter(
            object_id=self.xform.id, data_type='enketo_url')))

    def test_saving_same_metadata_object_doesnt_trigger_integrity_error(self):
        count = len(MetaData.objects.filter(object_id=self.xform.id,
                    data_type='enketo_url'))
        enketo_url = "https://dmfrm.enketo.org/webform"
        MetaData.enketo_url(self.xform, enketo_url)
        count += 1
        self.assertEquals(count, len(MetaData.objects.filter(
            object_id=self.xform.id, data_type='enketo_url')))

        MetaData.enketo_url(self.xform, enketo_url)
        self.assertEquals(count, len(MetaData.objects.filter(
            object_id=self.xform.id, data_type='enketo_url')))

    def test_unique_type_for_form(self):
        metadata = unique_type_for_form(
            self.xform, data_type='enketo_url',
            data_value="https://dmfrm.enketo.org/webform")

        self.assertIsInstance(metadata, MetaData)

        metadata_1 = unique_type_for_form(
            self.xform, data_type='enketo_url',
            data_value="https://dmerm.enketo.org/webform")

        self.assertIsInstance(metadata_1, MetaData)
        self.assertNotEqual(metadata.data_value, metadata_1.data_value)
        self.assertEqual(metadata.data_type, metadata_1.data_type)
        self.assertEqual(metadata.content_object, metadata_1.content_object)
