resource "aws_lb" "ecs_alb" {
  name               = "ecs-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.sg.id]
  subnets            = [aws_subnet.subnet_ecs.id, aws_subnet.subnet_ecs_2.id]
  tags = {
    Name = "ecs-alb"
  }
}

resource "aws_lb_target_group" "ecs_tg" {
  name        = "ecs-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip" 

  health_check {
    interval            = 30
    path                = "/"
    protocol            = "HTTP"
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "ecs_alb_listener" {
  load_balancer_arn = aws_lb.ecs_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ecs_tg.arn
  }

  depends_on = [aws_lb_target_group.ecs_tg]
}

resource "aws_autoscaling_group" "ecs_asg_maatalys" {
  vpc_zone_identifier = [ aws_subnet.subnet_ecs.id ]

  desired_capacity = 1
  max_size         = 2
  min_size         = 1

  launch_template {
    id      = aws_launch_template.ec2_lt_maatalys.id
    version = "$Latest"
  }

  tag {
    key                 = "AmazonECSManaged"
    value               = "true"
    propagate_at_launch = true
  }

  depends_on = [
    aws_lb.ecs_alb,
    aws_lb_target_group.ecs_tg,
    aws_lb_listener.ecs_alb_listener
  ]
}

resource "aws_ecs_cluster" "ecs_cluster_maatalys" {
  name = "ecs-cluster-${var.project_name}"
}

resource "aws_ecs_capacity_provider" "ecs_capacity_provider_maatalys" {
  name = "webapp-cp"

  auto_scaling_group_provider {
    auto_scaling_group_arn = aws_autoscaling_group.ecs_asg_maatalys.arn
    managed_scaling {
      maximum_scaling_step_size = 1000
      minimum_scaling_step_size = 1
      status                    = "ENABLED"
      target_capacity           = 100
    }
  }

  depends_on = [aws_ecs_cluster.ecs_cluster_maatalys]
}

resource "aws_ecs_task_definition" "ecs_task_definition_maatalys" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  cpu                      = "1024"
  memory                   = "512"

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

   container_definitions = jsonencode([
    {
      name      = "${var.project_name}-container"
      image     = var.image_url
      cpu       = 1024
      memory    = 512
      essential = true

      portMappings = [{
        containerPort = 80
        hostPort      = 80
        protocol      = "tcp"
      }]

      environment = [
        {
          name  = "SQLALCHEMY_DATABASE_URI"
          value = "postgresql+asyncpg://${var.db_username}:${var.db_password}@${aws_db_instance.postgres.address}:${aws_db_instance.postgres.port}/${var.db_name}"
        },
        { name = "DB_HOST",     value = aws_db_instance.postgres.address },
        { name = "DB_PORT",     value = tostring(aws_db_instance.postgres.port) },
        { name = "DB_NAME",     value = var.db_name },
        { name = "DB_USER",     value = var.db_username },
        { name = "DB_PASSWORD", value = var.db_password },

        { name = "DATABASE_ENGINE_POOL_SIZE",    value = "250" },
        { name = "DATABASE_ENGINE_MAX_OVERFLOW", value = "10" },
        { name = "DATABASE_ENGINE_POOL_PING",    value = "True" },

        # -- Logging & Auth --
        { name = "LOG_LEVEL",               value = "ERROR" },
        { name = "SECRET_KEY",              value = "123BADX" },
        { name = "ACCESS_TOKEN_EXPIRE_MINUTES", value = "3600" },
        { name = "ALGORITHM",               value = "HS256" },

        {
          name  = "KAFKA_CLUSTER_NAME"
          value = aws_msk_cluster.kafka.cluster_name
        },
        {
          name  = "KAFKA_BOOTSTRAP_SERVERS"
          value = aws_msk_cluster.kafka.bootstrap_brokers
        },
        { name = "KAFKA_SECURITY_PROTOCOL", value = "PLAINTEXT" },
        { name = "KAFKA_SASL_MECHANISM",    value = "" },
        { name = "KAFKA_SASL_USERNAME",     value = "" },
        { name = "KAFKA_SASL_PASSWORD",     value = "" },
        { name = "KAFKA_CLIENT_ID",         value = "maatalys-kafka" },

        { name = "AWS_REGION",              value = "us-east-2" },
      ]
    }
  ])
}

resource "aws_ecs_service" "ecs_service_maatalys" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.ecs_cluster_maatalys.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_maatalys.arn

  network_configuration {
    security_groups = [aws_security_group.sg.id]
    subnets         = [aws_subnet.subnet_ecs.id, aws_subnet.subnet_ecs_2.id]
  }

  force_new_deployment = true
    desired_count = 1

  triggers = {
    redeployment = timestamp()
  }

  capacity_provider_strategy {
    capacity_provider = aws_ecs_capacity_provider.ecs_capacity_provider_maatalys.name
    weight            = 100
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.ecs_tg.arn
    container_name   = "${var.project_name}-container"
    container_port   = 80
  }

  depends_on = [aws_autoscaling_group.ecs_asg_maatalys]

}

resource "aws_ecs_cluster_capacity_providers" "cluster_capacity_providers" {
  cluster_name = aws_ecs_cluster.ecs_cluster_maatalys.name

  capacity_providers = [aws_ecs_capacity_provider.ecs_capacity_provider_maatalys.name]

  default_capacity_provider_strategy {
    capacity_provider = aws_ecs_capacity_provider.ecs_capacity_provider_maatalys.name
    weight            = 100
  }
}
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}