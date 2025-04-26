from transforms.api import transform, Input
from palantir_models.transforms import ModelOutput
from main.model_adapters.adapter import SocialMediaAccountsAdapter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

@transform(
    training_data_input=Input("/Fall2025-1b832e/MisinformationDetection/SocialMediaThreatDetection/training_data"),
    model_output=ModelOutput("/Fall2025-1b832e/MisinformationDetection/SocialMediaThreatDetection/models/SocialMediaAccountClassifier"),
)
def compute(training_data_input, model_output):
    training_df = training_data_input.pandas()
    model = train_model(training_df)

    foundry_model = SocialMediaAccountsAdapter(model)

    model_output.publish(
        model_adapter=foundry_model,
    )


def train_model(training_df):
    X_train = training_df.drop(columns=["label", "account_id"])
    y_train = training_df["label"]

    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "clf",
                LogisticRegression(
                    solver="liblinear",
                    max_iter=1000,
                    class_weight="balanced"
                ),
            ),
        ]
    )

    pipe.fit(X_train, y_train)

    return pipe 
