provider "aws" {
  region = "us-east-1"
}

resource "aws_ecs_task_definition" "ftb_skies_definition" {
  family                   = "ftb-skies-family"
  cpu                      = 1024
  memory                   = 6144
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  container_definitions = jsonencode([
    {
      name      = "ftb-skies"
      image     = "${aws_ecr_repository.ftb_skies.repository_url}:latest"
      cpu       = 1024
      memory    = 6144
      essential = true
      portMappings = [
        {
          containerPort = 25565,
          hostPort      = 25565
        }
      ]
    }
  ])
}