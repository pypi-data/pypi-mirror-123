import catboost
import optuna
import logging
import optuna.trial
from catboost.utils import eval_metric
from sklearn.model_selection import train_test_split

logger = logging.getLogger('')
logger.setLevel(logging.INFO)


def catboost_model(model_type, df_features,
                   df_target, categorical_index, optimization_direction, catboost_metric,
                   out_dir="out", tmp_dir='_tmp'):
    logging.info("Initiating catboost modeling process...")

    def objective(trial):

        if model_type == 'Binary_Classification':
            param = {
                "objective": trial.suggest_categorical("objective", ["Logloss", "CrossEntropy"]),
                "colsample_bylevel": trial.suggest_float("colsample_bylevel", 0.01, 0.1),
                "depth": trial.suggest_int("depth", 1, 12),
                "boosting_type": trial.suggest_categorical("boosting_type", ["Ordered", "Plain"]),
                "bootstrap_type": trial.suggest_categorical("bootstrap_type", ["Bayesian", "Bernoulli", "MVS"]),
            }

            model = catboost.CatBoostClassifier(**param, cat_features=categorical_index, eval_metric=catboost_metric)
            X_train, X_valid, y_train, y_valid = train_test_split(df_features, df_target, test_size=0.25,
                                                                  stratify=df_target, random_state=17)

        elif model_type == 'Multiclass_Classification':
            param = {
                "loss_function": trial.suggest_categorical("loss_function", ["MultiClass"]),
                "colsample_bylevel": trial.suggest_float("colsample_bylevel", 0.01, 1.0),
                "depth": trial.suggest_int("depth", 1, 12),
                "leaf_estimation_method": trial.suggest_categorical("leaf_estimation_method", ["Newton"]),
                "boosting_type": trial.suggest_categorical("boosting_type", ["Ordered", "Plain"]),
                "bootstrap_type": trial.suggest_categorical("bootstrap_type", ["Bayesian", "Bernoulli", "MVS"]),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 1),
                "iterations": trial.suggest_int("iterations", 10, 100),
            }

            model = catboost.CatBoostClassifier(**param, cat_features=categorical_index,
                                                eval_metric=catboost_metric,
                                                objective="MultiClass")
            X_train, X_valid, y_train, y_valid = train_test_split(df_features, df_target, test_size=0.25,
                                                                  stratify=df_target, random_state=17)

        elif model_type == 'Regression':
            param = {
                "depth": trial.suggest_int("depth", 2, 10),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 1),
                "iterations": trial.suggest_int("iterations", 10, 100),
                "boosting_type": trial.suggest_categorical("boosting_type", ["Ordered", "Plain"]),

            }
            model = catboost.CatBoostRegressor(**param, cat_features=categorical_index,
                                               eval_metric=catboost_metric)
            X_train, X_valid, y_train, y_valid = train_test_split(df_features, df_target, test_size=0.25,
                                                                  random_state=17)
        else :
            logging.error("Invalid model_type")
            raise ImportError('Error: could not proceed')

        model.fit(X_train, y_train, eval_set=[(X_valid, y_valid)], verbose=0, early_stopping_rounds=100)
        predictions = model.predict(X_valid)
        return eval_metric(list(y_valid), list(predictions), catboost_metric)[0]

    study = optuna.create_study(direction=optimization_direction)
    optuna.logging.disable_default_handler()
    logging.info("Initiating model training...")
    logging.info("Training... in progress ...")
    study.optimize(objective, n_trials=100)
    logging.info("Fetching the best parameters...")
    trial = study.best_trial
    for key, value in trial.params.items():
        logging.info("    {}: {}".format(key, value))

    if model_type == 'Regression':
        return catboost.CatBoostRegressor(**study.best_params)

    return catboost.CatBoostClassifier(**study.best_params)
