
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

module "cosmosdb" {
  source              = "Azure/cosmosdb/azurerm"
  version             = "3.5.0"

  name                = var.cosmos_account_name
  location            = var.location
  resource_group_name = var.resource_group_name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  capabilities        = ["EnableServerless"]

  databases = [
    {
      name       = var.database_name
      throughput = 400
      containers = [
        {
          name               = var.container_name
          partition_key_path = "/customerId"
        }
      ]
    }
  ]
}
