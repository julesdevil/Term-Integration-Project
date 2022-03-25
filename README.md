gcloud builds submit --tag gcr.io/term-integration-project-gcp/dash-tip  --project=term-integration-project-gcp

gcloud run deploy --image gcr.io/term-integration-project-gcp/dash-tip --platform managed  --project=term-integration-project-gcp --allow-unauthenticated