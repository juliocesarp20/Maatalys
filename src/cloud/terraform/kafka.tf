resource "aws_subnet" "kafka_private_1" {
  vpc_id                   = aws_vpc.main.id
  cidr_block               = "10.0.2.0/24"
  availability_zone        = "us-east-2a"
  map_public_ip_on_launch  = false

  tags = {
    Name = "${var.project_name}-kafka-priv-1"
  }
}

resource "aws_subnet" "kafka_private_2" {
  vpc_id                   = aws_vpc.main.id
  cidr_block               = "10.0.3.0/24"
  availability_zone        = "us-east-2b"
  map_public_ip_on_launch  = false

  tags = {
    Name = "${var.project_name}-kafka-priv-2"
  }
}

resource "aws_security_group" "kafka_sg" {
  name        = "${var.project_name}-kafka-sg"
  description = "Allow ECS - MSK and inter-broker traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "ECS - Kafka"
    from_port       = 9092
    to_port         = 9092
    protocol        = "tcp"
    security_groups = [ aws_security_group.sg.id ]
  }

  ingress {
    description = "Inter-broker"
    from_port   = 9094
    to_port     = 9094
    protocol    = "tcp"
    self        = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-kafka-sg"
  }
}

resource "aws_msk_cluster" "kafka" {
  cluster_name           = "${var.project_name}-kafka"
  kafka_version          = "2.8.1"
  number_of_broker_nodes = 2

  broker_node_group_info {
    instance_type   = "kafka.t3.small"
    client_subnets  = [
      aws_subnet.kafka_private_1.id,
      aws_subnet.kafka_private_2.id,
    ]
    security_groups = [ aws_security_group.kafka_sg.id ]

    storage_info {
      ebs_storage_info {
        volume_size = 20
      }
    }
  }

  tags = {
    Name = "${var.project_name}-kafka"
  }
}
