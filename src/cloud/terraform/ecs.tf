resource "aws_lb" "ecs_alb" {
  name               = "ecs-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.sg.id]
  subnets            = [aws_subnet.subnet_ecs.id,aws_subnet.subnet_ecs_2.id]
  tags = {
    Name = "ecs-alb"
  }
}

resource "aws_lb_target_group" "ecs_tg" {
  name     = "ecs-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

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
}

resource "aws_autoscaling_group" "ecs_asg_maatalys" {
  vpc_zone_identifier = [
    aws_subnet.subnet_ecs.id
  ]

  desired_capacity = 0
  max_size         = 2
  min_size         = 0

  launch_template {
    id      = aws_launch_template.ec2_lt_maatalys.id 
    version = "$Latest"
  }

  tag {
    key                 = "AmazonECSManaged"
    value               = "true"
    propagate_at_launch = true
  }

  target_group_arns = [aws_lb_target_group.ecs_tg.arn]

  depends_on = [
    aws_lb.ecs_alb,
    aws_lb_target_group.ecs_tg,
    aws_lb_listener.ecs_alb_listener
  ]
}

resource "aws_ecs_cluster" "ecs_cluster_maatalys" {
  name = "ecs-cluster-maatalys"
}

resource "aws_ecs_capacity_provider" "ecs_capacity_provider_maatalys" {
  name = "webapp-cp"

  auto_scaling_group_provider {
    auto_scaling_group_arn = aws_autoscaling_group.ecs_asg_maatalys.id
    managed_scaling {
      maximum_scaling_step_size = 1000
      minimum_scaling_step_size = 1
      status                    = "ENABLED"
      target_capacity           = 100
    }
    
  } 
}

resource "aws_ecs_cluster_capacity_providers" "ecs_cluster_capacity_providers_maatalys" {
  cluster_name = aws_ecs_cluster.ecs_cluster_maatalys.name
  capacity_providers = [aws_ecs_capacity_provider.ecs_capacity_provider_maatalys.name]
  
  default_capacity_provider_strategy {
    base  = 1
    weight = 100
    capacity_provider = aws_ecs_capacity_provider.ecs_capacity_provider_maatalys.name
  }
}

resource "aws_ecs_task_definition" "ecs_task_definition_maatalys" {
  family                   = "webapp"
  network_mode             = "awsvpc"
  execution_role_arn       = "arn:aws:iam::187476123193:role/ecsInstanceRole"
  cpu                      = "1024"
  memory                   = "1024"

  runtime_platform {
   operating_system_family  = "LINUX"
   cpu_architecture         = "X86_64" 
  }

  container_definitions = jsonencode([{
    name      = "webapp-ctr"
    image     = "strm/helloworld-http"
    cpu       = 1024
    memory    = 256
    essential = true
    portMappings = [
      {
        containerPort = 80
        hostPort      = 80
        protocol      = "tcp"
      }
    ]
  }])
}

resource "aws_ecs_service" "ecs_service_maatalys" {
  name            = "webapp-svc"
  cluster         = aws_ecs_cluster.ecs_cluster_maatalys.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_maatalys.arn
  desired_count   = 2

  network_configuration {
    security_groups = [aws_security_group.sg.id]
    subnets          = [aws_subnet.subnet_ecs.id]
  }

  force_new_deployment = true
  placement_constraints {
    type = "distinctInstance"
  }

  triggers = {
    redeployment = timestamp()
  }
    capacity_provider_strategy {
      capacity_provider = aws_ecs_capacity_provider.ecs_capacity_provider_maatalys.name
      weight            = 100
    }

  load_balancer {
    target_group_arn = aws_lb_target_group.ecs_tg.arn
    container_name   = "webapp-ctr"
    container_port   = 80
  }

  depends_on = [aws_autoscaling_group.ecs_asg_maatalys]
}
