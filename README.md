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

- Add Write file S3 with API/Website
- Add Backup RDS
- Complete Documentation:
  - OIDC GitHub Action: https://xebia.com/blog/how-to-deploy-terraform-to-aws-with-github-actions-authenticated-with-openid-connect/
  - RDS setup
  - EC2 setup
  - Main Readme
- Terraform auto doc?