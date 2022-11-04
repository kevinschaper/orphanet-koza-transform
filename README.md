# orphanet-koza-transform
A quick one-off Koza transform of Orphanet gene to disease data

To make it do a thing:
 * poetry install
 * poetry run downloader
 * poetry run ./post-process.sh
 * poetry run koza transform --source transform/orphanet/gene_to_disease.yaml
 
