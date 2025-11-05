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

resource "google_bigquery_dataset" "feedback_dataset" {
  project       = var.project_id # Direct reference to the single project ID
  dataset_id    = replace("${var.project_name}_feedback", "-", "_")
  friendly_name = "${var.project_name}_feedback"
  location      = var.region
  depends_on    = [resource.google_project_service.project_services]

  labels = {
    "created-by" = "terraform"
    "purpose"    = "feedback-logs"
    "agent"      = var.project_name
  }
}

resource "google_bigquery_dataset" "telemetry_logs_dataset" {
  project       = var.project_id # Direct reference to the single project ID
  dataset_id    = replace("${var.project_name}_telemetry", "-", "_")
  friendly_name = "${var.project_name}_telemetry"
  location      = var.region
  depends_on    = [resource.google_project_service.project_services]

  labels = {
    "created-by" = "terraform"
    "purpose"    = "telemetry-logs"
    "agent"      = var.project_name
  }
}

resource "google_logging_project_sink" "feedback_export_to_bigquery" {
  name        = "${var.project_name}_feedback"
  project     = var.project_id # Direct reference to the single project ID
  destination = "bigquery.googleapis.com/projects/${var.project_id}/datasets/${google_bigquery_dataset.feedback_dataset.dataset_id}" # Direct reference
  filter      = var.feedback_logs_filter

  bigquery_options {
    use_partitioned_tables = true
  }

  unique_writer_identity = true # This will be the writer_identity for the single sink
  depends_on             = [google_bigquery_dataset.feedback_dataset] # Direct reference
}

resource "google_logging_project_sink" "log_export_to_bigquery" {
  name        = "${var.project_name}_telemetry"
  project     = var.project_id # Direct reference to the single project ID
  destination = "bigquery.googleapis.com/projects/${var.project_id}/datasets/${google_bigquery_dataset.telemetry_logs_dataset.dataset_id}" # Direct reference
  filter      = var.telemetry_logs_filter

  bigquery_options {
    use_partitioned_tables = true
  }

  unique_writer_identity = true # This will be the writer_identity for the single sink
  depends_on             = [google_bigquery_dataset.telemetry_logs_dataset] # Direct reference
}

resource "google_project_iam_member" "bigquery_data_editor" {
  # No for_each needed, as it's for the single project
  project = var.project_id # Direct reference to the single project ID
  role    = "roles/bigquery.dataEditor"
  member  = google_logging_project_sink.log_export_to_bigquery.writer_identity # Direct reference
}

resource "google_project_iam_member" "feedback_bigquery_data_editor" {
  # No for_each needed, as it's for the single project
  project = var.project_id # Direct reference to the single project ID
  role    = "roles/bigquery.dataEditor"
  member  = google_logging_project_sink.feedback_export_to_bigquery.writer_identity # Direct reference
}
