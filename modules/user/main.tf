
variable "username" {
  type        = string
  description = "Username of GitHub user"
}

output "username" {
  value = var.username
}
