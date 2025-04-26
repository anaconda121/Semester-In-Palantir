from transforms.api import transform, Input, Output

@transform(
    features_and_labels_input=Input("ri.foundry.main.dataset.f5c829e8-132a-4b3a-ad0f-677a2503dff0"),
    training_output=Output("/Fall2025-1b832e/MisinformationDetection/SocialMediaThreatDetection/training_data"),
    testing_output=Output("/Fall2025-1b832e/MisinformationDetection/SocialMediaThreatDetection/testing_data"),
)
def compute(features_and_labels_input, training_output, testing_output):
    features_and_labels = features_and_labels_input.dataframe()

    training_data, testing_data = features_and_labels.randomSplit([0.8, 0.2], seed=0)
    training_output.write_dataframe(training_data)
    testing_output.write_dataframe(testing_data)
