# EQUIDX AI — root Terraform configuration (AWS reference implementation).
# Provisions the networking, EKS cluster, and managed RDS Postgres that the
# infrastructure/k8s manifests deploy onto. Adapt provider/modules for GCP
# or Azure as needed — module interfaces are kept intentionally small.

terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }

  backend "s3" {
    bucket = "equidx-ai-terraform-state"
    key    = "equidx-ai/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source       = "./modules/vpc"
  environment  = var.environment
  cidr_block   = var.vpc_cidr
  az_count     = 3
}

module "eks" {
  source          = "./modules/eks"
  environment     = var.environment
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  cluster_version = var.kubernetes_version
  node_instance_types = var.node_instance_types
  min_nodes       = var.min_nodes
  max_nodes       = var.max_nodes
}

module "rds" {
  source            = "./modules/rds"
  environment       = var.environment
  vpc_id            = module.vpc.vpc_id
  subnet_ids        = module.vpc.private_subnet_ids
  db_name           = "equidx"
  db_username       = "equidx"
  instance_class    = var.rds_instance_class
  allocated_storage = var.rds_allocated_storage
}

resource "aws_s3_bucket" "uploads" {
  bucket = "equidx-ai-uploads-${var.environment}"

  tags = {
    Project     = "equidx-ai"
    Environment = var.environment
    Purpose     = "biosensor-raw-signal-and-file-uploads"
  }
}

resource "aws_s3_bucket_versioning" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "equidx-redis-${var.environment}"
  engine               = "redis"
  node_type            = var.redis_node_type
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  subnet_group_name    = module.vpc.elasticache_subnet_group_name
}
