## Terrarform actions


```sh
./terraform.sh \
  --platform aws\
  --env dev \
  --cmd validate
```

```sh
./terraform.sh \
  --platform aws\
  --env dev \
  --cmd plan
```

```sh
./terraform.sh \
  --platform aws\
  --env dev \
  --cmd apply
```

```sh
./terraform.sh \
  --platform aws\
  --env dev \
  --cmd destroy
```

```sh
tfsec .
```

```sh
terraform-docs markdown --recursive --output-file TF_DOC.md ./
```

- Complete Documentation:
  - OIDC GitHub Action: https://xebia.com/blog/how-to-deploy-terraform-to-aws-with-github-actions-authenticated-with-openid-connect/
  - RDS setup
  - EC2 setup
  - Main Readme