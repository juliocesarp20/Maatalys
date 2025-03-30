resource "aws_key_pair" "maatalys_ec2_key" {
  key_name   = "maatalys-ec2-key"
  public_key = file("~/.ssh/maatalys-ec2-key.pub")
}

resource "aws_launch_template" "ec2_lt_maatalys" {
  name_prefix          = "ecs-template-maatalys"
  image_id             = var.ami_maatalys
  instance_type        = var.instance_type
  key_name             = aws_key_pair.maatalys_ec2_key.key_name 
  vpc_security_group_ids = [aws_security_group.sg.id]

  iam_instance_profile  {
    name = "ecsInstanceRole"
  }
  
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "ecs_instance"
    }
  }
  user_data = filebase64("${path.module}/ecs.sh")
}
