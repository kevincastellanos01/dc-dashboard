# Infrastructure

La visión general del proyecto está en [README.es.md](../README.es.md).

Terraform in this folder creates the AWS footprint the container runs on. GitHub Actions does not create that footprint. After the test job passes, Actions builds an image, pushes it to the repository this stack created, and forces a new deployment of the service that already exists.

## Resources

Defined in `main.tf`:

- ECR repository, mutable tags, scan on push
- ECS cluster, Fargate task definition, and service
- Application Load Balancer, IP target group, HTTP listener on port 80
- Security groups: the load balancer accepts TCP 80 from the internet; tasks accept TCP 8501 only from that load balancer
- CloudWatch log group `/ecs/<project_name>` with 7-day retention
- IAM execution role for the agent, and a task role for the container

The target group health check is Streamlit's `/_stcore/health`, which is the same path the image `HEALTHCHECK` uses.

Tasks get a public IP so they can pull the image without a NAT gateway. Inbound traffic is still limited to the load balancer security group. The listener is HTTP on port 80. TLS would be another listener and a certificate, and this stack does not create either.

## Variables

| Name | Default | Role |
| --- | --- | --- |
| `aws_region` | `us-east-1` | Region for every resource |
| `project_name` | `kevin-dc` | Prefix for the repository, cluster, service, and load balancer |
| `task_cpu` | `256` | Fargate CPU units |
| `task_memory` | `512` | Fargate memory, MiB |
| `desired_count` | `1` | Number of tasks |

Copy `terraform.tfvars.example` to `terraform.tfvars` to override them. `terraform.tfvars` is gitignored.

The names in `.github/workflows/deploy.yml` are the defaults above: repository `kevin-dc-repo`, cluster `kevin-dc-cluster`, service `kevin-dc-service`, region `us-east-1`. If you change `project_name` or the region, update that workflow in the same change. Renaming them in a stack that is already applied replaces resources.

## Use

Credentials for the AWS provider come from the environment or a shared config file. This folder does not store keys.

```bash
cd infra
terraform init
terraform plan
terraform apply
terraform output app_url
```

The provider lock file (`.terraform.lock.hcl`) is committed so `terraform init` resolves the same AWS provider. State files are not committed.

## Deploy workflow

`.github/workflows/deploy.yml` has two jobs:

1. **Test.** Installs `requirements-dev.txt` on Python 3.11 and runs `pytest`. Pull requests stop here.
2. **Deploy to ECS.** Runs on a push to `main`, and only if Test succeeded. It logs in with the repository secrets `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, pushes `linux/amd64` to ECR as `:latest`, and calls `aws ecs update-service --force-new-deployment`.

The workflow authenticates with long-lived access keys. OpenID Connect is the replacement when those keys should go away. That change is an IAM change, not a dashboard change, so it is not wired here.

## Cost

An internet-facing load balancer and a running Fargate task are billed while they exist. `terraform destroy` removes the stack when you no longer want it running.
