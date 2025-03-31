resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    name = "main"
  }
}

resource "aws_subnet" "subnet_ecs" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.0.0/24"
  map_public_ip_on_launch = true
  availability_zone = "us-east-2a"

  tags = {
    Name = "subnet_ecs"
  }
}

resource "aws_subnet" "subnet_ecs_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone = "us-east-2b"

  tags = {
    Name = "subnet_ecs_2"
  }
}

resource "aws_security_group" "sg" {
  name        = "allow_http_https"
  description = "Allow HTTP and HTTPS inbound, all outbound"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

resource "aws_route_table" "rtb" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "main-route-table"
  }
}

resource "aws_route_table_association" "rta_subnet_ecs" {
  subnet_id      = aws_subnet.subnet_ecs.id
  route_table_id = aws_route_table.rtb.id
}

resource "aws_route_table_association" "rta_subnet_ecs_2" {
  subnet_id      = aws_subnet.subnet_ecs_2.id
  route_table_id = aws_route_table.rtb.id
}
