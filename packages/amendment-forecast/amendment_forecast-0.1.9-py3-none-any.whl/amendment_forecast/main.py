# main runner
import pandas as pd
from dateutil.relativedelta import relativedelta

from amendment_forecast import utils
from amendment_forecast.models import DATE_COLUMN_NAME, VALUE_COLUMN_NAME, initialize_model

FREQUENCY_MAPPING = {
    "week": "W-MON",
    "month": "MS"
}


def get_train_end_date(time_series_df, training_holdout):
    """ Determines the start date for the test data and throws a warning if less than 1 year of training data is included
    """
    training_rows = int(len(time_series_df) * training_holdout)
    train_end_date = time_series_df.iloc[training_rows][DATE_COLUMN_NAME]

    if (train_end_date - time_series_df[DATE_COLUMN_NAME].min()).days < 365:
        print("Warning: Less than 1 year of data provided for training")

    return train_end_date


def run_forecast_ensemble(
        dataframe,
        date_column,
        target_column,
        forecast_horizon_years,
        aggregate_operation="sum",
        training_holdout_pct=0.3,
        frequency="week",
        period_format=None,
        model_list=None):
    # Initialize with copy of input date
    df = dataframe.copy()
    df[DATE_COLUMN_NAME] = pd.to_datetime(df[date_column])

    # Creates time series and ensures proper naming and frequency
    frequency = FREQUENCY_MAPPING.get(frequency)
    df = utils.create_time_series_from_records(
        df,
        target_column,
        aggregate_operation,
        period_format)
    df = df[[DATE_COLUMN_NAME, VALUE_COLUMN_NAME]]

    # Create Future Forecast Periods
    start_date = pd.to_datetime(dataframe[DATE_COLUMN_NAME]).max() + relativedelta(days=1)
    end_date = start_date + relativedelta(years=forecast_horizon_years)
    period_list = pd.date_range(start=start_date, end=end_date, freq=frequency)

    # Mark dataframe with training/testing split
    train_end_date = get_train_end_date(df, training_holdout_pct)

    # Assemble ensemble of models
    if model_list:
        named_model_list = model_list
    else:
        named_model_list = [
            "GreyKite",
            "FBProphet",
            "Naive",
            "XGBoost",
            "RandomForest",
            "SARIMA"
        ]

    # For each model, run a full evaluation and add to the ensemble results
    ensemble = []
    for model_name in named_model_list:
        print(f"    Running --{model_name}")
        model_dict = {"name": model_name}
        model = initialize_model(model_name)
        results = model.evaluate(
            dataframe=df,
            train_end_date=train_end_date,
            frequency=frequency,
            forecast_period_list=period_list)
        model_dict["train_timestamps"] = results.pop("train_timestamps")
        model_dict["prediction_values"] = results.pop("prediction_values")
        model_dict["actual_values"] = results.pop("actual_values")
        model_dict["forecast_timestamps"] = results.pop("forecast_timestamps")
        model_dict["forecast_values"] = results.pop("forecast_values")
        model_dict["performance_metrics"] = results
        weight = model_dict["performance_metrics"]["r2"]
        if weight < 0:
            weight = 0
        model_dict["weight"] = weight
        ensemble.append(model_dict)

    # Combine outputs to calculate ensemble effectiveness
    total_weight = sum([model["weight"] for model in ensemble])
    ensemble_predictions_list = []
    ensemble_forecast_list = []
    for model in ensemble:
        model["weight"] = model["weight"] / total_weight
        if model["weight"] > 0:
            predictions = pd.Series(model["prediction_values"]).reset_index(drop=True) * model["weight"]
            forecast = pd.Series(model["forecast_values"]).reset_index(drop=True) * model["weight"]
            actuals = pd.Series(model["actual_values"])
            ensemble_predictions_list.append(predictions)
            ensemble_forecast_list.append(forecast)
    ensemble_train_timestamps = model["train_timestamps"]
    ensemble_predictions = sum(ensemble_predictions_list)
    ensemble_actuals = model["actual_values"]
    ensemble_forecast_timestamps = model["forecast_timestamps"]
    ensemble_forecast = sum(ensemble_forecast_list)

    ensemble_train_df = pd.DataFrame({
        "timestamps": ensemble_train_timestamps,
        "actuals": ensemble_actuals,
        "predictions": ensemble_predictions})
    ensemble_forecast_df = pd.DataFrame({
        "timestamps": ensemble_forecast_timestamps,
        "forecast": ensemble_forecast_timestamps})
    ensemble_train_df = ensemble_train_df[~ensemble_train_df.predictions.isnull()]
    performance_metrics = utils.get_model_statistics(ensemble_train_df["predictions"], ensemble_train_df["actuals"])
    consolidated_metrics = utils.consolidate_scores(performance_metrics, ensemble_train_df["actuals"].mean())

    degraded_accuracies = {}
    training_years = (df[DATE_COLUMN_NAME].max() - df[DATE_COLUMN_NAME].min()).days / 365
    for year in range(1, forecast_horizon_years + 1):
        multiplier = 1.0
        years_outside_of_training = max(year - training_years, 0)
        if years_outside_of_training > 0:
            for yy in range(1, int(year) + 1):
                if yy > (2 * training_years):
                    multiplier *= 0.5
                elif yy > training_years:
                    multiplier *= 0.95
        degraded_accuracies[year] = multiplier * consolidated_metrics["accuracy"]

    ensemble.append({
        "name": "ensemble",
        "model": None,
        "train_dataframe": ensemble_train_df,
        "forecast_dataframe": ensemble_forecast_df,
        "performance_metrics": performance_metrics,
        "consolidated_metrics": consolidated_metrics,
        "weight": None
    })

    return ensemble
