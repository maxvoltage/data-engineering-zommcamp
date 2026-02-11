# Terraform Configuration for Data Engineering Zoomcamp

This directory contains the Terraform configuration files to set up the infrastructure on Google Cloud Platform (GCP).

## Prerequisites

1.  **GCP Account**: A Google Cloud Platform account.
2.  **Service Account**: A service account with the necessary permissions (e.g., Editor or specific roles for Storage and BigQuery).
3.  **Credentials Key**: A JSON key file for the service account, placed in the `terraform/keys/` directory.

## Getting Started

### 1. Project Structure

- `main.tf`: Defines the GCP provider and resources.
- `variables.tf`: Declares the variables used in the configuration.
- `terraform.tfvars`: Contains the values for the variables (Sensitive data, should be ignored by git).
- `keys/`: Directory for service account JSON keys (Ignored by git).

### 2. Configuration (`terraform.tfvars`)

The `terraform.tfvars` file is used to manage sensitive information and project-specific configurations. To set up your credentials, ensure your `terraform.tfvars` file contains the path to your service account key:

```hcl
google_credentials = "path/to/your/service-account-key.json"
```

> **Note**: This file is automatically loaded by Terraform. It is included in `.gitignore` to prevent secret leakage.

### 3. Usage

Initialize Terraform to install the necessary providers:
```bash
terraform init
```

Preview the infrastructure changes:
```bash
terraform plan
```

Apply the changes to create the infrastructure:
```bash
terraform apply
```

To destroy the infrastructure:
```bash
terraform destroy
```

## Security Best Practices

- Never commit your `terraform.tfvars` or any file inside the `keys/` directory.
- The `.gitignore` file in this directory is configured to exclude these sensitive files.
