import palantir_models as pm

from palantir_models_serializers import DillSerializer

class SocialMediaAccountsAdapter(pm.ModelAdapter):

    @pm.auto_serialize(model=DillSerializer())
    def __init__(self, model):
        self.model = model

    @classmethod
    def api(cls):
        # input-output API
        columns = [
            ("primary_platform", int),
            ("account_age_days", int),
            ("verified_flag", int),
            ("followers_cnt", int),
            ("base_post_rate", float),
            ("prior_flags_cnt", int),
            ("strike_count", int),
            ("avg_daily_likes", int),
            ("avg_daily_reshares", int),
            ("avg_daily_comments", int)
        ]
        inputs = {
            "df_in": pm.Pandas(columns),
        }
        outputs = {
            "df_out": pm.Pandas(columns + [("prediction", float)])
        }
        return inputs, outputs

    def predict(self, df_in):
        # generate predict using input features
        df_in["prediction"] = self.model.predict(
            df_in[["primary_platform", "account_age_days", "verified_flag",
                "followers_cnt", "base_post_rate", "prior_flags_cnt",
                "strike_count", "avg_daily_likes", "avg_daily_reshares",
                "avg_daily_comments"]]
        )
        return df_in
