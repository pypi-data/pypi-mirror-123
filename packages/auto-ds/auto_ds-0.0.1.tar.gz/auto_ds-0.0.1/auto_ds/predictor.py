from sklearn.base import BaseEstimator
from .autods import AutoDS
from .models.catboost_method import catboost_model
from .models.catboost_utils import fetch_catboost_eval_metric, get_optimization_direction
from .utils import generate_categorical_features, remove_cols,   impute_missing_category,read_data
import pandas as pd
import logging

logger = logging.getLogger('')
logger.setLevel(logging.INFO)


class AutoDSPredictor(BaseEstimator):
    autods_object: AutoDS

    def __init__(self, autods_object, model='', df_test_features=pd.DataFrame()):

        self.model = model
        self.df_test_features = df_test_features
        self.autods_object = autods_object
        self.df_features = self.autods_object.df_features
        self.df_target = self.autods_object.df_target
        self.categorical_index = self.autods_object.categorical_index
        self.metric = self.autods_object.metric
        self.model_type = self.autods_object.model_type


        self.id_cols = self.autods_object.id_cols
        self.obj_cols = self.autods_object.obj_cols
        self.excess_missing_cols = self.autods_object.excess_missing_cols
        self.id_n_dup_cols = self.autods_object.id_n_dup_cols

        # self.text_fields = self.autods_object.text_fields
        #
        self.ext = self.autods_object.ext

        self.categorical_candidates = self.autods_object.categorical_candidates
        self.categorical_index = self.autods_object.categorical_index
        # self.max_missing_count = self.autods_object.max_missing_count
        # self.object_category_count = self.autods_object.object_category_count
        self.is_imbalance = self.autods_object.is_imbalance
        self.index_col = self.autods_object.index_col
        self.text_vector = self.autods_object.text_vector

    def _clean_test_data(self,):
        remove_cols(self.df_test_features, self.obj_cols + self.id_n_dup_cols + self.id_cols + self.excess_missing_cols)
        self.df_test_features = generate_categorical_features(self.df_test_features, self.categorical_candidates)
        if self.categorical_index:
            impute_missing_category(self.df_test_features, self.categorical_index)

    def _model(self) -> object:
        catboost_metric = fetch_catboost_eval_metric(self.metric)
        optimization_direction = get_optimization_direction(catboost_metric)


        model = catboost_model(self.model_type,self.df_features,
                                             self.df_target, self.categorical_index,
                                             optimization_direction, catboost_metric)

        return model

    def fit(self):
        if self.categorical_index:
            impute_missing_category(self.df_features, self.categorical_index)

        # what if numeric feature is missing ?
        # right now its only cat boost which can handle missing values

        logging.info('Building models ..')
        self.model = self._model()
        self.model.fit(X=self.df_features, y=self.df_target, cat_features=self.categorical_index)
        return self

    def predict(self, path):
        self.df_test_features = read_data(path, self.ext)
        self._clean_test_data()

        return self.model.predict(self.df_test_features)
