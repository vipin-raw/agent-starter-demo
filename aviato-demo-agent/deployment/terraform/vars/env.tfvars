# Project name used as a base for resource naming
project_name = "aviato-demo-agent"

# The Google Cloud region you will use to deploy the infrastructure
region = "us-central1"

# The single Google Cloud Project ID for all resources
project_id = "aviato-ai-code"

# Name of the host connection you created in Cloud Build
host_connection_name = "git-aviato-demo-agent"
github_pat_secret_id = "github_pat"

repository_owner = "jinay-aviato"

# Name of the repository you added to Cloud Build
repository_name = "agent-starter-demo"

# Set to false because the connection does NOT exist and needs to be created by Terraform
create_cb_connection = false

# The installation ID for the GitHub App. From your terraform plan.
github_app_installation_id = "93005766"
