platform=""
env=""
cmd=""

# FUNCTIONS
usage() {
  echo "Terraform commands wrapper" >&2
  echo "usage : $0 --platform <ptf> --env <env> --cmd <cmd>" >&2
  echo "--platform aws or gcp" >&2
  echo "--env      terraform environment" >&2
  echo "--cmd      terraform command to play"
  exit 0
}

##################################################################
### MAIN
##################################################################
# Parse arguments
echo "$@"
while [ $# -gt 0 ]; do
  case $1 in
  --platform)
    platform=$2
    shift 2
    ;;
  --env)
    env=$2
    shift 2
    ;;
  --cmd)
    cmd=$2
    shift 2
    ;;
  -h | -help | --help) usage ;;
  *) break ;;
  esac
done

echo "Initialise terraform: "
echo "TF_IN_AUTOMATION=true TF_DATA_DIR=\"/envs/${env}/.terraform\" terraform -chdir=\"${platform}\" init --backend-config=\"$(pwd)/${platform}/backend.tfvars\""
TF_IN_AUTOMATION=true TF_DATA_DIR="envs/${env}/.terraform" terraform -chdir="${platform}" init --backend-config="$(pwd)/${platform}/backend.tfvars"

echo "$cmd terraform: "

if [ $cmd = "output" ]; then
  echo "TF_DATA_DIR=\"envs/${env}/.terraform\" terraform \"${cmd}\""
  TF_DATA_DIR="envs/${env}/.terraform" terraform "${cmd}"
elif [ "$cmd" = "validate" ]; then
  echo "TF_DATA_DIR=\"envs/${env}/.terraform\" terraform -chdir=\"${platform}\" \"${cmd}\""
  TF_DATA_DIR="envs/${env}/.terraform" terraform -chdir="${platform}" "${cmd}"
else
  echo "TF_DATA_DIR=\"envs/${env}/.terraform\" terraform -chdir=\"${platform}\" \"${cmd}\" -var-file \"$(pwd)/${platform}/envs/${env}/config.tfvars\" -var-file \"$(pwd)/${platform}/envs/common.tfvars\""
  TF_DATA_DIR="envs/${env}/.terraform" terraform -chdir="${platform}" "${cmd}" -var-file "$(pwd)/${platform}/envs/${env}/config.tfvars" -var-file "$(pwd)/${platform}/envs/common.tfvars"
fi
