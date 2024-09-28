## Terrarform actions


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