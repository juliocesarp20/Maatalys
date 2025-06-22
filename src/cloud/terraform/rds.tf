
resource "aws_subnet" "rds_private_1" {
  vpc_id                   = aws_vpc.main.id
  cidr_block               = "10.0.4.0/24"
  availability_zone        = "us-east-2a"
  map_public_ip_on_launch  = false

  tags = {
    Name        = "${var.project_name}-${var.environment}-rds-priv-1"
    Environment = var.environment
  }
}

resource "aws_subnet" "rds_private_2" {
  vpc_id                   = aws_vpc.main.id
  cidr_block               = "10.0.5.0/24"
  availability_zone        = "us-east-2b"
  map_public_ip_on_launch  = false

  tags = {
    Name        = "${var.project_name}-${var.environment}-rds-priv-2"
    Environment = var.environment
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "${var.project_name}-${var.environment}-rds-sg"
  description = "Allow inbound from ECS on 5432"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Postgres from ECS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [ aws_security_group.sg.id ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-rds-sg"
    Environment = var.environment
  }
}

resource "aws_db_subnet_group" "rds_subnets" {
  name       = "${var.project_name}-${var.environment}-db-subnet"
  subnet_ids = [
    aws_subnet.rds_private_1.id,
    aws_subnet.rds_private_2.id,
  ]

  tags = {
    Name        = "${var.project_name}-${var.environment}-db-subnet"
    Environment = var.environment
  }
}

resource "aws_db_instance" "postgres" {
  identifier                 = "${var.project_name}-${var.environment}-postgres"
  engine                     = "postgres"
  engine_version             = var.db_engine_version
  instance_class             = var.db_instance_class
  allocated_storage          = var.db_allocated_storage
  storage_encrypted          = true

  username                   = var.db_username
  password                   = var.db_password
  db_name                    = var.db_name          

  db_subnet_group_name       = aws_db_subnet_group.rds_subnets.name
  vpc_security_group_ids     = [ aws_security_group.rds_sg.id ]
  publicly_accessible        = false
  skip_final_snapshot        = true
  backup_retention_period    = 7
  auto_minor_version_upgrade = true
  deletion_protection        = false

  tags = {
    Name        = "${var.project_name}-${var.environment}-postgres"
    Environment = var.environment
  }
}
