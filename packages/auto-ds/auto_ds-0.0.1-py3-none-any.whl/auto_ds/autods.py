from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from .utils import is_imbalance_classification, fetch_model_type, fetch_excessive_missing_cols, \
    separate_text_from_data, process_train_text, fetch_categorical_candidates, \
    read_data_into_features_n_target, add_index, fetch_id_and_duplicate_cols, generate_categorical_features, \
    fetch_remaining_obj_cols, remove_cols, fetch_categorical_index, concat_data_and_text, process_date_fields
import logging

logger = logging.getLogger('')
logger.setLevel(logging.INFO)

class AutoDS(BaseEstimator):

    def __init__(self, data, target, metric='', text_fields=[], datetime_fields= [], id_cols=[],
                 numeric_category_threshold=10, missing_threshold=0.4,
                 object_to_category_threshold=0.25, text_vector=TfidfVectorizer()):

        #  target amd metric are mandatory
        logging.info('Welcome to Auto Data Science framework');
        logging.info('Initializing AutoDS object...')

        # this assignment is actually not required ?
        self.data = data

        logging.info('Setting target variable as... ' + str(target))
        self.target = target

        self.metric = metric
        logging.info('Setting  text fields as... ' + str(text_fields))
        self.text_fields = text_fields
        self.date_fields = datetime_fields

        # TODO: instead of hardcoded in init  use a configuration file ?
        self.numeric_category_threshold = numeric_category_threshold
        self.missing_threshold = missing_threshold
        self.object_to_category_threshold = object_to_category_threshold
        self.text_vector = text_vector

        # optional user configurable fields
        self.id_cols = id_cols

        # assigning default values which would be computed programmatically later on
        self.is_imbalance = False
        self.categorical_candidates = []
        self.categorical_index = []

        # derived parameters
        self.ext = self.data.split('.')[-1]
        logging.info('Setting file extension as...' + str(self.ext))

        self.df_features, self.df_target = read_data_into_features_n_target(data, target, self.ext)

        if self.date_fields:
            self.df_features= process_date_fields(self.df_features,self.date_fields )


        if self.text_fields:
            logging.info('Vectorising text fields... ')
            self.df_features, self.df_text = separate_text_from_data(self.df_features, self.text_fields)
            self.text_vector, self.df_text = process_train_text(self.df_text)

        self.max_missing_count = int(self.df_features.shape[0] * missing_threshold)
        logging.info('Setting threshold for missing feature values to ... ' + str(self.max_missing_count))
        self.object_category_count = int(self.df_features.shape[0] * object_to_category_threshold)

        self.excess_missing_cols = fetch_excessive_missing_cols(self.df_features, self.max_missing_count)

        # system will automatically find model type
        self.model_type = fetch_model_type(self.df_target, self.numeric_category_threshold)

        logging.info('Setting problem type to ... ' + str(self.model_type))
        # check if problem is of imbalance class
        if self.model_type != 'Regression':
            self.is_imbalance = is_imbalance_classification(self.df_target)

        #  assign default  metric if not there
        if not metric:
            if self.model_type == "Regression":
                self.metric = 'rmse'
            else:
                self.metric = 'accuracy'

        # find out id column & duplicate columns if not specified
        self.index_col = []
        self.id_n_dup_cols = []
        if not self.id_cols:
            self.index_col = ['index_col_0', 'index_col_1']
            self.df_features = add_index(self.df_features)
            self.id_n_dup_cols = fetch_id_and_duplicate_cols(self.df_features)

        # before calculating categorical columns drop unwanted features
        remove_cols(self.df_features, self.index_col + self.id_n_dup_cols + self.id_cols + self.excess_missing_cols)

        self.categorical_candidates = fetch_categorical_candidates(self.df_features, self.object_category_count,
                                                                   self.numeric_category_threshold)
        if self.categorical_candidates:
            logging.info('Setting categorical columns ... ' + str(self.categorical_candidates))
            self.df_features = generate_categorical_features(self.df_features, self.categorical_candidates)

        self.obj_cols = fetch_remaining_obj_cols(self.df_features)

        if self.obj_cols:
            logging.info('Removing object columns ... ' + str(self.obj_cols))
            remove_cols(self.df_features, self.obj_cols)

        if self.categorical_candidates:
            self.categorical_index = fetch_categorical_index(self.df_features)
            logging.info('Setting categorical feature indexes as ... ' + str(self.categorical_index))

        if self.text_fields:
            logging.info('concatenating vectorized text features ... ' + str(self.categorical_index))
            self.df_features = concat_data_and_text(self.df_features, self.df_text)
