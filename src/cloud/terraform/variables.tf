variable "ami_maatalys" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "maatalys"
}

variable "image_url" {
  description = "Nome base da imagem Docker"
  type        = string
  default     = "maatalys:latest"
}

