# modules


`modules` is a sub-repository for tfmodules.


## Creating a new terraform module


The `./bin/create_module.py` file is a nice helper for quickly stubbing out a new terraform module. It accepts a `--name` arg and includes a `--help` flag if you find yourself stuck:


```
./bin/create_module.py --help

usage: TfModule-ater [-h] --name NAME

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  The name of the module to create.
```

**Creating a new module is straightforward:**


```
./bin/create_module.py --name spiffy

Creating spiffy tf module...
Creating spiffy/test/main.tf...
Creating spiffy/main.tf...
Creating spiffy/variables.tf...
Creating spiffy/outputs.tf...
```


If a module already exists, `create_module` quickly short-circuits:


```
./bin/create_module.py --name spiffy

The spiffy module already exists. Not creating...
```


## Testing terraform modules during development


Each module in this repository should have a corresponding `test` directory. This enables module developers to quickly set up and iterate upon modules without impacting other infrastructure or pushing to git and waiting for atlantis to pick up changes. Another benefit to the `test/` directory is it gives other developers a reference for using the respective module.


To get started with an example, `cd` to `spiffy/test` and run `terraform init && terraform apply`:

```
$ cd spiffy/test

$ terraform init && terraform apply

Initializing modules...

Initializing the backend...

Initializing provider plugins...
- Reusing previous version of hashicorp/google from the dependency lock file
- Using previously-installed hashicorp/google v3.71.0

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
var.yourname
  your name, plz

  Enter a value: jp


Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # module.spiffy.google_pubsub_topic.notification_topic will be created
  + resource "google_pubsub_topic" "notification_topic" {
      + id      = (known after apply)
      + labels  = {
          + "env"          = "dev-jp"
          + "stewarded-by" = "platform-team"
          + "system"       = "spiffy"
        }
      + name    = "dev-jp-spiffy-bag-notifications"
      + project = (known after apply)
...
...
```


**NOTE!!! When testing terraform modules, please clean up after yourself with a `terraform destroy`!!!**


## Using and tagging terraform modules


### Using


When calling these modules from elsewhere, you'll need to use a source call that looks like the following:

```
module "spiffy" {
   source = "git@github.com:johncassil/terraform-infra.git//modules/mymodule?ref=1.0.0"
   somevar="this"
}
```

..where `?ref=` is the specific version you want to deploy.


**To check which version is the most recent, use `git describe --tag`:**


```
$ git describe --tag
v0.0.3
```

**To list all tags, use `git tag -n`:**


```
$ git tag -n 
0.0.1           "some description"
v0.0.1          "some desc"
v0.0.2          some description for 0.0.2
v0.0.3          more testing
```


### Incrementing and Tagging Versions


`./bin/version.py` from the repository root gives you a little helper for versioning code, checking existing version (if you don't want to look at the `.VERSION` file), and pushing reftags. It comes with its own `--help` flag if you are stuck:


```
./bin/version.py --help
usage: TFModules Versioner [-h] --command {check,bump,reftag} [--version_type {major,minor,patch}]

optional arguments:
  -h, --help            show this help message and exit
  --command {check,bump,reftag}, -c {check,bump,reftag}
                        The command to run.
  --version_type {major,minor,patch}, -t {major,minor,patch}
                        Which version type to increment or check. Ignored when using the `reftag` command.
```


**To increment the patch, use `./bin/version.py --command bump` or `/bin/version.py --command bump --version_type patch`:**


```
$ ./bin/version.py --command bump
Please provide a description for this version: trying this out for the README

$ git status
On branch DP-94
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   .CHANGELOG
	modified:   .VERSION
```


The `.CHANGELOG` will be appended to and the `.VERSION` file will be appropriately incremented.


**After your branch is merged to main, the corresponding reftag (from `.VERSION`) will be pushed to git**:


```
$ git tag -n
0.0.1           "some description"
v0.0.1          "some desc"
v0.0.2          some description for 0.0.2
v0.0.3          more testing
v0.0.4          some desc for a reftag
```


### The Changelog


The `.CHANGELOG` file in the repository root is automatically generated via the `./bin/version.py` helper mentioned above. If you are interested in seeing how the tfmodules repository has evolved over time, take a peek!
