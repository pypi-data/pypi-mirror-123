import unittest
import uuid

from ibm_watson_machine_learning.helpers.connections import DataConnection, ContainerLocation
from ibm_watson_machine_learning.utils.autoai.errors import WMLClientError
from ibm_watson_machine_learning.tests.utils import bucket_exists, create_bucket, is_cp4d, save_data_to_container
from ibm_watson_machine_learning.tests.autoai.abstract_tests_classes import AbstractTestAutoAIAsync, \
    AbstractTestWebservice, AbstractTestBatch

from ibm_watson_machine_learning.utils.autoai.enums import PredictionType, Metrics, ClassificationAlgorithms


class TestAutoAIRemoteFairness(AbstractTestAutoAIAsync, unittest.TestCase):
    """
    The test can be run on CLOUD, and CPD
    """

    cos_resource = None
    data_location = './autoai/data/drug_train_data_updated.csv'

    data_cos_path = 'data/drug_train_data_updated.csv'

    SPACE_ONLY = False

    OPTIMIZER_NAME = "Drug data test sdk"

    HISTORICAL_RUNS_CHECK = False

    target_space_id = None

    fairness_info = {
        # "protected_attributes": [
        #     {"feature": "SEX", "privileged_groups": ['F']},
        #     {"feature": "BP", "privileged_groups": ["LOW", "NORMAL"]}
        # ],
        "favorable_labels": ["drugA", "drugC"]
    }

    experiment_info = dict(
        name=OPTIMIZER_NAME,
        desc='FAIRNESS experiment',
        prediction_type=PredictionType.MULTICLASS,
        prediction_column='DRUG',
        scoring=Metrics.RECALL_SCORE_WEIGHTED,
        include_only_estimators=[ClassificationAlgorithms.LGBM,
                                 ClassificationAlgorithms.XGB],
        fairness_info=fairness_info,
        max_number_of_estimators=2,
        text_processing=False
    )


    def test_00b_write_data_to_container(self):
        if self.SPACE_ONLY:
            self.wml_client.set.default_space(self.space_id)
        else:
            self.wml_client.set.default_project(self.project_id)

        save_data_to_container(self.data_location, self.data_cos_path, self.wml_client)

    def test_00c_check_fairness_info(self):
        print(self.fairness_info)

        self.assertIn('favorable_labels', self.fairness_info)
        self.assertIsInstance(self.fairness_info['favorable_labels'], list)

    def test_02_data_reference_setup(self):
        TestAutoAIRemoteFairness.data_connection = DataConnection(
            location=ContainerLocation(path=self.data_cos_path
                                       ))
        TestAutoAIRemoteFairness.results_connection = None

        self.assertIsNotNone(obj=TestAutoAIRemoteFairness.data_connection)
        self.assertIsNone(obj=TestAutoAIRemoteFairness.results_connection)

    def test_10_summary_listing_all_pipelines_from_wml(self):
        TestAutoAIRemoteFairness.summary = self.remote_auto_pipelines.summary()
        print(TestAutoAIRemoteFairness.summary)
        self.assertIn('holdout_disparate_impact', list(TestAutoAIRemoteFairness.summary.columns))
        self.assertIn('training_disparate_impact', list(TestAutoAIRemoteFairness.summary.columns))


        for col in self.summary.columns:
            print(self.summary[col])

    def test_99_delete_connection_and_connected_data_asset(self):
        if not self.SPACE_ONLY:
            self.wml_client.set.default_project(self.project_id)
        self.wml_client.connections.delete(self.connection_id)

        with self.assertRaises(WMLClientError):
            self.wml_client.connections.get_details(self.connection_id)


class TestFairnessNumericalValues(TestAutoAIRemoteFairness):
    fairness_info = {
        "protected_attributes": [
            # {"feature": "AGE", "privileged_groups": [18, [38, 50], 60]},
            {"feature": "CHOLESTEROL", "privileged_groups": [[0, 0.7], 0.613261]}
        ],
        "favorable_labels": ["drugA"]
    }
    experiment_info = dict(
        name="Fairness",
        desc='FAIRNESS experiment',
        prediction_type=PredictionType.MULTICLASS,
        prediction_column='DRUG',
        scoring=Metrics.ACCURACY_SCORE,
        include_only_estimators=[ClassificationAlgorithms.SnapDT],
        fairness_info=fairness_info,
        notebooks=True,
        max_number_of_estimators=1,
        text_processing=False
    )



if __name__ == '__main__':
    unittest.main()
