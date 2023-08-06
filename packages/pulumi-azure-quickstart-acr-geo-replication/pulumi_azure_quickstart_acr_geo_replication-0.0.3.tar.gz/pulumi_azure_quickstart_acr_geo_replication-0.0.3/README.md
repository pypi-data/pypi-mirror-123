# Azure Container Registry Geo Replication Multi-Lang Component (Go)

This repo provides an Azure Container Registry Geo Replication Pulumi Component.
Even though the component itself is written in Go, it is consumable from any
language Pulumi supports.

An example `Registry` [component
resource](https://www.pulumi.com/docs/intro/concepts/resources/#components) is
available in `provider/pkg/provider/registryGeoReplication.go`. This component
provides a new Azure Container Registry with geo-replication.

Note that the generated provider plugin (`pulumi-resource-azure-quickstart-acr-geo-replication`) must be on your `PATH` to be used by Pulumi deployments. If creating a provider for distribution to other users, you should ensure they install this plugin to their `PATH`.

## Prerequisites

- Go 1.15
- Pulumi CLI
- Node.js (to build the Node.js SDK)
- Yarn (to build the Node.js SDK)
- Python 3.6+ (to build the Python SDK)
- .NET Core SDK (to build the .NET SDK)

## Build and Test

```bash
# Build and install the provider (plugin copied to $GOPATH/bin)
make install_provider

# Regenerate SDKs
make generate

# Test Node.js SDK
$ make install_nodejs_sdk
$ cd examples/simple
$ yarn install
$ yarn link @pulumi/acrgeoreplication
$ pulumi stack init test
$ pulumi up
```


## Thoughts before publishing

- Should we give the user the ability to choose the `Sku`? It must be `Premium`
  to allow this feature.
- Should we have the user pass in the name of the resource group, or the
  resource group itself (as a ref)?
- Do the dotnet example
  
## Just After Publishing
- Update `requirments.txt` to be accurate.
