import unittest
import uuid

from ibm_watson_machine_learning.helpers.connections import DataConnection, S3Location, ContainerLocation
from ibm_watson_machine_learning.utils.autoai.errors import WMLClientError
from ibm_watson_machine_learning.tests.utils import save_data_to_container, create_bucket, is_cp4d, \
    create_connection_to_cos
from ibm_watson_machine_learning.tests.autoai.abstract_tests_classes import AbstractTestAutoAIAsync, \
    AbstractTestWebservice, AbstractTestBatch

from ibm_watson_machine_learning.utils.autoai.enums import PredictionType, Metrics, RegressionAlgorithms


class TestAutoAIRemote(AbstractTestAutoAIAsync, AbstractTestWebservice, unittest.TestCase):
    """
    The test can be run on CLOUD, and CPD
    """

    cos_resource = None
    data_location = './autoai/data/insurance.csv'

    data_cos_path = 'insurance.csv'
    results_cos_path = "results"
    # batch_payload_location = './autoai/data/drug_train_data_updated_scoring_payload.csv'
    # batch_payload_cos_location = 'scoring_payload/drug_train_data_updated_scoring_payload.csv'

    SPACE_ONLY = False

    OPTIMIZER_NAME = "Insurance data Fairness test sdk"

    # BATCH_DEPLOYMENT_WITH_DF = True
    # BATCH_DEPLOYMENT_WITH_DA = False
    HISTORICAL_RUNS_CHECK = False

    target_space_id = None

    fairness_info = {
        "protected_attributes": [
            {"feature": "sex", "reference_group": ['male']},
            {"feature": "age", "reference_group": [[20, 40], [60, 90]]}
        ],
        "favorable_labels": [[1000.0, 5000.0]]}

    experiment_info = dict(
        name=OPTIMIZER_NAME,
        desc='FAIRNESS experiment',
        prediction_type=PredictionType.REGRESSION,
        prediction_column='charges',
        scoring="r2_and_disparate_impact",
        include_only_estimators=[RegressionAlgorithms.SnapRF,
                                 RegressionAlgorithms.SnapBM],
        fairness_info=fairness_info,
        max_number_of_estimators=2,
        notebooks=True,
        text_processing=True
    )

    def test_00b_write_data_to_container(self):
        if self.SPACE_ONLY:
            self.wml_client.set.default_space(self.space_id)
        else:
            self.wml_client.set.default_project(self.project_id)

        save_data_to_container(self.data_location, self.data_cos_path, self.wml_client)

    def test_00c_prepare_COS_instance_and_connection(self):
        TestAutoAIRemote.connection_id, TestAutoAIRemote.bucket_name = create_connection_to_cos(
            wml_client=self.wml_client,
            cos_credentials=self.cos_credentials,
            cos_endpoint=self.cos_endpoint,
            bucket_name=self.bucket_name,
            save_data=True,
            data_path=self.data_location,
            data_cos_path=self.data_cos_path)

        self.assertIsInstance(self.connection_id, str)

    def test_02_data_reference_setup(self):
        TestAutoAIRemote.data_connection = DataConnection(
            location=ContainerLocation(path=self.data_cos_path
                                       ))

        TestAutoAIRemote.results_connection = DataConnection(
            connection_asset_id=self.connection_id,
            location=S3Location(
                bucket=self.bucket_name,
                path=self.results_cos_path
            )
        )

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)
        self.assertIsNotNone(obj=TestAutoAIRemote.results_connection)

    def test_10_summary_listing_all_pipelines_from_wml(self):
        TestAutoAIRemote.summary = self.remote_auto_pipelines.summary()
        print(TestAutoAIRemote.summary)
        self.assertIn('holdout_disparate_impact', list(TestAutoAIRemote.summary.columns))
        self.assertIn('training_disparate_impact', list(TestAutoAIRemote.summary.columns))

        for col in self.summary.columns:
            print(self.summary[col])

    # def test_99_delete_connection_and_connected_data_asset(self):
    #     if not self.SPACE_ONLY:
    #         self.wml_client.set.default_project(self.project_id)
    #     self.wml_client.connections.delete(self.connection_id)
    #
    #     with self.assertRaises(WMLClientError):
    #         self.wml_client.connections.get_details(self.connection_id)


if __name__ == '__main__':
    unittest.main()
