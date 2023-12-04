pytest:
	pytest tests

tf-init:
	terraform -chdir=./terraform init

infra-up-plan:
	terraform -chdir=./terraform plan

infra-up:
	terraform -chdir=./terraform apply

infra-down:
	terraform -chdir=./terraform destroy
