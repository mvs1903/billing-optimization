
variable "location" {
  type    = string
  default = "East US"
}

variable "resource_group_name" {
  type = string
}

variable "storage_account_name" {
  type = string
}

variable "container_name" {
  type    = string
  default = "archived-billing-records"
}
