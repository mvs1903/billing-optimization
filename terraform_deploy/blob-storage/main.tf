
provider "azurerm" {
  features {}
}

module "storage" {
  source              = "Azure/storage-account/azurerm"
  version             = "3.8.0"

  name                = var.storage_account_name
  resource_group_name = var.resource_group_name
  location            = var.location
  account_tier        = "Standard"
  account_replication_type = "LRS"
  containers = [
    {
      name                  = var.container_name
      container_access_type = "private"
    }
  ]
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}
