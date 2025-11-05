# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 1. Assign roles to the CICD runner service account
resource "google_project_iam_member" "cicd_runner_sa_roles" {
  for_each = toset(var.cicd_roles)

  project    = var.project_id
  role       = each.key # Use each.key for toset
  member     = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
  depends_on = [resource.google_project_service.project_services]

}

# 2. Grant application SA the required permissions to run the application
resource "google_project_iam_member" "app_sa_roles" {
  count      = length(var.app_sa_roles) # Use count for a list of roles
  project    = var.project_id # Direct reference to the single project ID
  role       = var.app_sa_roles[count.index] # Access role by index
  member     = "serviceAccount:${google_service_account.app_sa.email}" # Direct reference to the single app_sa
  depends_on = [resource.google_project_service.project_services]
}


# 3. Allow Cloud Run service SA to pull containers stored in the CICD project
resource "google_project_iam_member" "cicd_run_invoker_artifact_registry_reader" {
  project    = var.project_id # Direct reference to the single project ID
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:service-${data.google_project.main_project_data.number}@serverless-robot-prod.iam.gserviceaccount.com" # Access the single project data
  depends_on = [resource.google_project_service.project_services]

}

# 4. Allow the CICD SA to act as the Application SA during Cloud Run deployments
resource "google_service_account_iam_member" "cicd_can_act_as_app_sa" {
  service_account_id = google_service_account.app_sa.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.cicd_runner_sa.email}"
  depends_on = [
    google_service_account.app_sa,
    google_service_account.cicd_runner_sa
  ]
}



# Special assignment: Allow the CICD SA to create tokens
resource "google_service_account_iam_member" "cicd_run_invoker_token_creator" {
  service_account_id = google_service_account.cicd_runner_sa.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
  depends_on         = [resource.google_project_service.project_services]
}
# Special assignment: Allow the CICD SA to impersonate himself for trigger creation
resource "google_service_account_iam_member" "cicd_run_invoker_account_user" {
  service_account_id = google_service_account.cicd_runner_sa.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
  depends_on         = [resource.google_project_service.project_services]
}
