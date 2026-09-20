from azure.storage.blob import BlobServiceClient
from getpass import getpass
from pathlib import Path
import argparse

CONTAINER = "fraud-data"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--model-path",
    type=str,
    default=None,
    help="Optional path to fraud_lr_model.pkl"
)
args = parser.parse_args()

connection_string = getpass("Paste Azure Storage connection string: ")
blob_service = BlobServiceClient.from_connection_string(connection_string)
container = blob_service.get_container_client(CONTAINER)

uploads = {
    "raw/creditcard_sample.csv": Path("creditcard_sample.csv"),
    "processed/creditcard_sample.csv": Path("creditcard_sample.csv"),
}

if args.model_path:
    uploads["models/fraud_lr_model.pkl"] = Path(args.model_path)

for blob_name, local_path in uploads.items():
    if not local_path.exists():
        print(f"SKIPPED - local file missing: {local_path}")
        continue

    with open(local_path, "rb") as f:
        container.upload_blob(
            name=blob_name,
            data=f,
            overwrite=True
        )

    print(f"Uploaded: {blob_name}")

blob = container.get_blob_client("raw/creditcard_sample.csv")
downloaded = blob.download_blob().readall()

print()
print("Read-back successful")
print("Downloaded bytes:", len(downloaded))

print()
print("Current Blob layout:")
for item in container.list_blobs():
    if item.name.startswith(("raw/", "processed/", "models/")):
        print("-", item.name)