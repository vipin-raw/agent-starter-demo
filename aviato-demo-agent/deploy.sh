#!/bin/bash
#
# This script deploys the agent to Google Cloud Run.
#
# USAGE:
#   1. Set your Project ID:
#      gcloud config set project YOUR_PROJECT_ID_HERE
#   2. Run the script:
#      ./deploy.sh

# --- Configuration ---
export PROJECT_ID=$(gcloud config get-value project)
export REGION="australia-southeast1" # Sydney region, as requested
export SERVICE_NAME="proactive-sales-agent"
export IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

echo "----------------------------------------------------"
echo "Deploying Agent: ${SERVICE_NAME}"
echo "Project:     ${PROJECT_ID}"
echo "Region:      ${REGION}"
echo "Image:       ${IMAGE_NAME}"
echo "----------------------------------------------------"

# 1. Enable necessary Google Cloud services
echo "Enabling required services..."
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  iam.googleapis.com

# 2. Build the Docker image using Google Cloud Build
# This reads your new Dockerfile, builds it in the cloud, and tags it
echo "Building Docker image..."
gcloud builds submit . --tag ${IMAGE_NAME}

# 3. Deploy the image to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --region ${REGION} \
  --platform "managed" \
  --allow-unauthenticated \
  --project ${PROJECT_ID} \
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=True"

# After deployment, Cloud Run will provide a service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')

echo "----------------------------------------------------"
echo "✅ Deployment complete!"
echo "Your agent is now running at: ${SERVICE_URL}"
echo "----------------------------------------------------"