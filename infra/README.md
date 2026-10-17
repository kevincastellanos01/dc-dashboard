# Infrastructure

La visión general del proyecto está en [README.es.md](../README.es.md).

Terraform in this folder can create an AWS footprint for the container. Nothing in GitHub Actions applies it. Running `terraform apply` creates resources that AWS bills until you destroy them.

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

Copy `terraform.tfvars.example` to `terraform.tfvars` to override them. `terraform.tfvars` and the state files are gitignored. Do not commit them. The state file is the map of real resources, and it does not belong in a public repository.

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

## Cost

An internet-facing load balancer and a running Fargate task are billed while they exist. `terraform destroy` removes the stack when you no longer want it running.
