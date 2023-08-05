import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import os
import shutil
from datetime import datetime

import logging
logger = logging.getLogger('')
logger.setLevel(logging.INFO)




def read_data(file_path, ext):
    if ext == 'csv':
        df_data = pd.read_csv(file_path)
    # to do add other file formats as well
    elif ext == 'xlsx':
        df_data = pd.read_excel(file_path)
    else :
        logging.error("Auto ds currently supports csv and xslx file extension. Looks like your files has different "
                      "extesion. ")
    return  df_data


def read_data_into_features_n_target(data_path, target_column, ext):
    df_data = read_data(data_path, ext)
    df_target = df_data[target_column]
    df_features = df_data.drop([target_column], axis=1, errors='ignore')
    del df_data
    return df_features, df_target



#  to fetch  id and duplicate columns
def fetch_id_and_duplicate_cols(df, index_col= ['index_col_0', 'index_col_1'] ):
    # Create an empty set
    duplicateColumnSet = set()
    # Iterate through all the columns
    # of dataframe
    for x in range(df.shape[1]):
        # Take column at xth index.
        col = df.iloc[:, x]
        # Iterate through all the columns in
        # DataFrame from (x + 1)th index to
        # last index
        for y in range(x + 1, df.shape[1]):
            # Take column at yth index.
            otherCol = df.iloc[:, y]
            # Check if two columns at x & y
            # index are equal or not,
            # if equal then adding
            # to the set
            if col.equals(otherCol):
                duplicateColumnSet.add((df.columns.values[y], df.columns.values[x]))
    id_and_dup_cols = []
    for c1, c2 in duplicateColumnSet:
        if c1 in index_col:
            id_and_dup_cols.append(c2)
        else:
            id_and_dup_cols.append(c1)
    return id_and_dup_cols


def add_index(data, index_col=['index_col_0', 'index_col_1']):
    data[index_col[0]] = data.index
    data[index_col[1]] = data.index + 1
    return data


#  which problem type it is
def fetch_model_type(df_target, numeric_category_threshold):
    if df_target.nunique() == 2:
        problem_type = "Binary_Classification"
    elif df_target.dtype != 'O' and df_target.nunique() > numeric_category_threshold:
        problem_type = "Regression"
    else:
        problem_type = "Multiclass_Classification"
    logging.info("Problem is of type " + problem_type +
                 " ..if it is not correct kindly rerun by specifying problem type")
    return problem_type


def get_catboost_eval_metric(problem_type, metric):
    if (metric != ''):
        return metric
    elif problem_type == "Regression":
        metric = 'root_mean_squared_error'
    else:
        metric = 'accuracy'
    return metric


def segregate_feature_target(df, target_column):
    target = df[target_column]
    features = df.drop([target_column], axis=1, errors='ignore')
    return features, target


def is_missing(df):
    return df.isnull().values.any()


def fetch_numeric_cols(df):
    return list(df._get_numeric_data().columns)


def fetch_missing_cols(df):
    feature_missingcounts = df.isna().sum()
    i = 0
    missing_cols = []
    for v in feature_missingcounts:
        if v > 0:
            missing_cols.append(feature_missingcounts.index[i])
        i = i + 1

    return (missing_cols)


# example ['Sex', 'Embarked']
def fetch_categorical_candidates(df, object_category_threshold, numeric_category_threshold):
    # categorical column can be object as well as numerical
    num_cols = df._get_numeric_data().columns
    obj_cols = list(df.select_dtypes(include='object').columns)

    categorical_candidates = []
    for col in num_cols:
        if df[col].nunique() < numeric_category_threshold and df[col].isnull().values.any():
            categorical_candidates.append(col)

    for col in obj_cols:
        if df[col].nunique() < object_category_threshold:
            categorical_candidates.append(col)

    return categorical_candidates


def generate_categorical_features(df, category_features):
    for col in category_features:
        logging.info("the col processing is : " + col)
        # if df[col].dtype == 'float64':
        #     df[col] = df[col].astype('int')
        if df[col].dtype == 'O':
            df[col] = df[col].astype('str')
        df[col] = df[col].astype('category')
        # LabelEncoder().fit_transform(df[col])
    return df


def fetch_remaining_obj_cols(df):
    return list(df.select_dtypes(include=['object']).columns)


def remove_cols(df, obj_cols):
    df.drop(obj_cols, axis=1, inplace=True, errors='ignore')


def missing_numeric_treatment():
    return


def text_feature_treatment():
    pass


def is_imbalance_classification(df_target):
    # highest to lowes ratio should be greater than 10 for imbalance label
    ratio = df_target.value_counts().tolist()[0] / df_target.value_counts().tolist()[-1]
    if ratio > 10:
        return True
    return False


def fetch_excessive_missing_cols(df, max_missing_count):
    excessive_missing_cols = []
    for col in df.columns:
        if df[col].isnull().values.any():
            if df[col].isnull().sum() > max_missing_count:
                excessive_missing_cols.append(col)
    return excessive_missing_cols


def fetch_categorical_index(df_features):
    categorical_index = []
    i = 0
    for col in df_features.columns:
        if df_features[col].dtypes.name == 'category':
            categorical_index.append(i)
        i = i + 1
    return categorical_index


def impute_missing_category(df, cat_features_no):
    # options add new category as missing
    for col_no in cat_features_no:
        if is_missing(df[df.columns[col_no]]):
            df[df.columns[col_no]] = df[df.columns[col_no]].cat.add_categories('MISSING')
            df[df.columns[col_no]] = df[df.columns[col_no]].fillna('MISSING')


def data_split(X, y, test_size=0.25):
    X_train, X_valid, y_train, y_valid = train_test_split(X, y,
                                                          test_size=test_size,
                                                          stratify=y,
                                                          random_state=17)
    return X_train, X_valid, y_train, y_valid



def model_evaluate(model, features_df, target, metric, cross_validation):
    mesure = cross_val_score(model, features_df, target, cv=cross_validation, scoring=metric)
    mesure_mean = mesure.mean()
    logging.info(" Fold Cross-Validation " + metric + " measure is : " + str(mesure_mean))
    return mesure_mean


def create_clean_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        shutil.rmtree(folder_name)
        os.makedirs(folder_name)


# to add all catboost metric


def generate_submission_file(test_df, model, id_column, id_values, target, out_dir="out"):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    pred = model.predict(test_df)
    sub = pd.DataFrame()
    sub[id_column] = id_values
    sub[target] = pred
    sub.to_csv(out_dir + "/baseline_submission.csv", index=False)

    logging.info("Submission File Generated, here is the snapshot: ")
    logging.info(sub.head(10))


# before
def separate_text_from_data(df_features, text_fields):
    df_text = pd.DataFrame()
    df_text['corpus'] = df_features[text_fields].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
    df_features.drop(text_fields, axis=1, errors='ignore', inplace=True)
    return df_features, df_text


# after
def concat_data_and_text(data_df, text_df):
    df_feature = pd.concat([data_df, text_df], axis=1)
    return df_feature


def process_train_text(text_df):
    # choose one among tfid or countvectorizer
    tf_victories = TfidfVectorizer(min_df=3, max_features=None,
                                   strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                                   ngram_range=(1, 3), use_idf=1, smooth_idf=1, sublinear_tf=1,
                                   stop_words='english')

    # count_vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1))
    train_countvectors = tf_victories.fit_transform(list(text_df['corpus'].values))
    vectorized_text_df = pd.DataFrame.sparse.from_spmatrix(train_countvectors)
    return tf_victories, vectorized_text_df


def process_test_text(text_df, tf_victories):
    # choose one among tfid or countvectorizer
    # count_vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1))
    test_vectors = tf_victories.transform(list(text_df['corpus'].values))
    vectorized_text_df = pd.DataFrame.sparse.from_spmatrix(test_vectors)
    return tf_victories, vectorized_text_df


def process_test_text(text_df, vectorizer):
    train_countvectors = vectorizer.transform(list(text_df['corpus'].values))
    vectorized_text_df = pd.DataFrame.sparse.from_spmatrix(train_countvectors)
    return vectorized_text_df


# convert datatime to int how ?
def process_datetime (datetime_object ):
    return (datetime.today() - datetime_object).days

def process_date_fields( df_features, date_fields ):
    for field in date_fields:
        df_features[field]=df_features[field].apply(lambda x: process_datetime(x))
    return df_features

