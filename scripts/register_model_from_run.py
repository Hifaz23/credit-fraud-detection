from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
from azure.identity import InteractiveBrowserCredential

SUBSCRIPTION_ID = "b3910179-0857-4bff-bb51-0566ca37632b"
RESOURCE_GROUP = "rg-fraud-mlops-g9"
WORKSPACE_NAME = "mlw-fraud-mlops-g9"

JOB_ID = "f0afc93c-e8ef-4b75-8a0a-6df086a6bad1"

credential = InteractiveBrowserCredential(
    tenant_id="bba41668-b4a5-4352-a4e8-6fb246f74ffa"
)

ml_client = MLClient(
    credential=credential,
    subscription_id=SUBSCRIPTION_ID,
    resource_group_name=RESOURCE_GROUP,
    workspace_name=WORKSPACE_NAME,
)

model = Model(
    name="fraud-lr-azure-demo",
    version="3",
    type=AssetTypes.CUSTOM_MODEL,
    path=f"azureml://jobs/{JOB_ID}/outputs/model_output",
    description="G9 candidate produced by successful Azure ML gated pipeline run.",
    tags={
        "project": "G9",
        "source": "gated_pipeline",
        "validation_gate": "passed",
        "model_type": "logistic_regression",
    },
)

registered = ml_client.models.create_or_update(model)

print("Registered model:", registered.name)
print("Version:", registered.version)
print("Model ID:", registered.id)