resource "aws_security_group" "example" {
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "example" {
  instance_type = "t3.large"
}
