variable "environment" { type = string }
variable "vpc_id" { type = string }
variable "subnet_ids" { type = list(string) }
variable "cluster_version" { type = string }
variable "node_instance_types" { type = list(string) }
variable "min_nodes" { type = number }
variable "max_nodes" { type = number }
