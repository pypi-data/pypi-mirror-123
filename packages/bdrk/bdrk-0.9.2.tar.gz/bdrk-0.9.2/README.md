[Bedrock](https://bedrock.basis-ai.com) helps data scientists own the end-to-end deployment of machine learning workflows. `bdrk` is the official client library for interacting with APIs on Bedrock platform.

## Documentation

Full documentation and tutorials on Bedrock can be found [here](https://docs.basis-ai.com/)

## Usage

In order to use `bdrk`, you need to register an account with Basis AI. Please email `contact@basis-ai.com` to get started. Once an account is created, you will be issued a personal API token that you can use to authenticate with Bedrock.

### Installing Bedrock client

You can install Bedrock client library from PyPi with the following command. We recommend running it in a virtual environment to prevent potential dependency conflicts.

```bash
pip install bdrk
```

Note that the client library is officially supported for python 3.7 and above.

#### Installing optional dependencies

The following optional dependencies can be installed to enable additional featues.

Command line support:

```bash
pip install bdrk[cli]
```

Model monitoring support:

```bash
pip install boxkite
```

### Setting up your environment

Once installed, you need to add a well formed `bedrock.hcl` configuration file in your project's root directory. The configuration file specifies which script to run for training and deployment as well as their respective base Docker images. You can find an example directory layout [here](https://github.com/basisai/churn_prediction).

When using the module locally, you may need to define the following environment variables for `bdrk` to make API calls to Bedrock. These variables will be automatically set on your workload container when running in cluster.

```bash
export BEDROCK_API_DOMAIN=https://api.bdrk.ai
export BEDROCK_API_TOKEN=<your personal API token>
```

### Training on Bedrock

The `bdrk` library provides utility functions for your training runs.

#### Logging training metrics

You can easily export training metrics to Bedrock by adding logging code to `train.py`. The example below demonstrates logging charts and metrics for visualisation on Bedrock platform.

```python
import bdrk

bdrk.init()
with bdrk.start_run():
    bdrk.log_metric("Accuracy", 0.97)
    bdrk.log_binary_classifier_metrics([0, 1, 1], [0.1, 0.7, 0.9])
```

#### Logging feature and inference distribution

You may use the model monitoring service to save the distribution of input and model output data to a local file. The default path is `/artefact/histogram.prom` so as to bundle the computed distribution together with the model artefact it trained from. When trained on Bedrock, the zipped `/artefact` directory will be uploaded to user's blob storage bucket in the workload cluster.

```python
import pandas as pd
from boxkite.monitoring.service import ModelMonitoringService
from sklearn.svm import SVC

# User code to load training data
features = pd.DataFrame({'a': [1, 2, 3], 'b': [3, 2, 1]})
model = SVC(probability=True)
model.fit(features, [False, True, False])
inference = model.predict_proba(features)[:, 0]

ModelMonitoringService.export_text(
    features=features.iteritems(),
    inference=inference.tolist(),
)
```

#### Logging explainability and fairness metrics

Bedrock offers facility to generate and log explainability and fairness (XAFAI) metrics. `bdrk` provides an easy to use API and native integration with Bedrock platform to visualize XAFAI metrics. All data is stored in your environment's blob storage to ensure nothing leaves your infrastructure. Under the hood it uses [shap](https://github.com/slundberg/shap) library to provide both global and individual explainability, and [AI Fairness 360 toolkit](https://github.com/Trusted-AI/AIF360) to compare model behaviors between groups of interest for fairness assessment.

```python
# As part of your train.py
from bdrk.model_analyzer import ModelAnalyzer, ModelTypes

# Background data is used to simulate "missing" features to measure the impact.
# It is limited to maximum of 5000 rows by default to speed up analysis.
background = x_train

# Tree model: xgboost, lightgbm. Other types of model, including Tensorflow
# and Pytorch are also supported.
analyzer = ModelAnalyzer(
  model,
  'credit_risk_tree_model',
  model_type=ModelTypes.TREE,
).train_features(background).test_features(x_validation)

# Metrics are calculated and uploaded to blob storage
analyzer.analyze()
```

### Training locally

The `bdrk` library supports tracking runs outside of Bedrock platform.

```python
import bdrk

bdrk.init(project_id="test-project")
with bdrk.start_run(pipeline_id="local-pipeline", environment_id="canary-dev"):
    bdrk.download_model(model_id="colour", version=1)
    # ...
    # Training code goes here
    # ...
    bdrk.log_params({"alpha": 0.5, "l5_ratio": 0.5})
    bdrk.log_metrics(metrics={"metric_1": 0.5, "metric_2": 0.8})
    bdrk.log_binary_classifier_metrics(actual=[0, 1, 1], probability=[0, 0.1, 0.5])
    bdrk.log_model("./train.zip")
```

Under the hood, `bdrk.backend` module exposes APIs for interacting with Bedrock platform.

```python
from bdrk.backend.v1 import ApiClient, Configuration, PipelineApi
from bdrk.backend.v1.models import (
    PipelineResourcesSchema,
    TrainingPipelineRunSchema,
)

configuration = Configuration()
configuration.api_key["X-Bedrock-Access-Token"] = "MY-TOKEN"
configuration.host = "https://api.bdrk.ai"

api_client = ApiClient(configuration)
pipeline_api = PipelineApi(api_client)

pipeline = pipeline_api.get_training_pipeline_by_id(pipeline_id="MY-PIPELINE")
run_schema = TrainingPipelineRunSchema(
    environment_public_id="MY-ENVIRONMENT",
    resources=PipelineResourcesSchema(cpu="500m", memory="200M"),
    script_parameters={"MYPARAM": "1.23"},
)
run = pipeline_api.run_training_pipeline(
    pipeline_id=pipeline.public_id, training_pipeline_run_schema=run_schema
)
```

### Monitoring models in production

At serving time, users may import `boxkite` library to track various model performance metrics. Anomalies in these metrics can help inform users about model rot.

#### Logging predictions

The model monitoring service may be instantiated in serve.py to log every prediction request for offline analysis. The following example demonstrates how to enable prediction logging in a typical Flask app.

```python
from boxkite.monitoring.service import ModelMonitoringService
from flask import Flask, request
from sklearn.svm import SVC

# User code to load trained model
model = SVC(probability=True)
model.fit([[1, 3], [2, 2], [3, 1]], [False, True, False])

app = Flask(__name__)
monitor = ModelMonitoringService()

@app.route("/", methods=["POST"])
def predict():
    # User code to load features
    features = [2.1, 1.8]
    score = model.predict_proba([features])[:, 0].item()

    monitor.log_prediction(
        request_body=request.json,
        features=features,
        output=score,
    )
    return {"True": score}
```

The logged predictions are persisted in low cost blob store in the workload cluster with a maximum TTL of 1 month. The blob store is partitioned by the endpoint id and the event timestamp according to the following structure: `models/predictions/{endpoint_id}/2020-01-22/1415_{logger_id}-{replica_id}.txt`.

- Endpoint id is the first portion of your domain name hosted on Bedrock
- Replica id is the name of your model server pod
- Logger id is a Bedrock generated name that's unique to the log collector pod

These properties are injected automatically into your model server container as environment variables.

To minimize latency of request handling, all predictions are logged asynchronously in a separate thread pool. We measured the overhead along critical path to be less than 1 ms per request.

#### Tracking feature and inference drift

If training distribution metrics are present in `/artefact` directory, the model monitoring service will also track real time distribution of features and inference results. This is done using the same `log_prediction` call so users don't need to further instrument their serving code.

In order to export the serving distribution metrics, users may add a new `/metrics` endpoint to their Flask app. By default, all metrics are exported in Prometheus exposition format. The example code below shows how to extend the logging predictions example to support this use case.

```python
@app.route("/metrics", methods=["GET"])
def get_metrics():
    """Returns real time feature values recorded by prometheus
    """
    body, content_type = monitor.export_http(
        params=request.args.to_dict(flat=False),
        headers=request.headers,
    )
    return Response(body, content_type=content_type)
```

When deployed in your workload cluster, the `/metrics` endpoint is automatically scraped by Prometheus every minute to store the latest metrics as timeseries data.
