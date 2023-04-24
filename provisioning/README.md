# provisioning


A sub-repository for provisioning data and analytics systems (with terraform).


## Provisioning New Modules


**A `./bin/provision.py` helper exists to quickly stub out appropriate directory structure and `main.tf` file(s):**


```
./bin/provision.py --help

usage: provision.py [-h] --groups {platform-team,devops-team} [{platform-team,devops-team} ...] --envs {dev,stg,prd} [{dev,stg,prd} ...] --systems SYSTEMS [SYSTEMS ...]

optional arguments:
  -h, --help            show this help message and exit
  --groups {platform-team,devops-team} [{platform-team,devops-team} ...], -g {platform-team,devops-team} [{platform-team,devops-team} ...]
                        The groups in which to provision modules
  --envs {dev,stg,prd} [{dev,stg,prd} ...], -e {dev,stg,prd} [{dev,stg,prd} ...]
                        The envs in which to provision modules
  --systems SYSTEMS [SYSTEMS ...], -s SYSTEMS [SYSTEMS ...]
                        The terraform modules to provision
```


**For example, if you want to provision a terraform module titled `spiffy` from modules across `dev-platform-team`, `stg-platform-team`, and `prd-platform-team` it is as easy as `./bin/provision.py --groups platform-team --envs dev stg prd --systems spiffy`:**


```
~/t/provisioning ❯❯❯ ./bin/provision.py --groups platform-team --envs dev stg prd --systems spiffy
Setting up group=platform-team env=dev system=spiffy
platform-team/dev/spiffy/main.tf doesn't exist. Creating...
platform-team/dev/spiffy/outputs.tf doesn't exist. Creating...
Setting up group=platform-team env=stg system=spiffy
platform-team/stg/spiffy/main.tf doesn't exist. Creating...
platform-team/stg/spiffy/outputs.tf doesn't exist. Creating...
Setting up group=platform-team env=prd system=spiffy
platform-team/prd/spiffy/main.tf doesn't exist. Creating...
platform-team/prd/spiffy/outputs.tf doesn't exist. Creating...
```


**The directory structure will be automatically ensured and `main.tf` will be appropriately generated:**


```
cat platform-team/dev/spiffy/main.tf
terraform {
  backend "gcs" {
    bucket = "platform-team-terraform-state"
    prefix = "platform-team/dev/spiffy/tfstate.json"
  }
}

provider "google" {
  project = "dev-platform-team"
  region  = "us-central1"
  zone    = "us-central1-b"
}

module "spiffy" {
    source          = "git@github.com:johncassil/terraform-infra.git//modules/spiffy?ref=1.0.2" # FIXME! Use appropriate version
    env             = "dev"
    system          = "spiffy"
    stewarded_by    = "platform-team"
    # FIXME! Add additional module variables here.
}

```

