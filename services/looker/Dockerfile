FROM docker.sendgrid.net/sendgrid/dev_go-1.10

COPY . /opt/go/src/github.com/sendgrid/dx-automator/services/looker

WORKDIR /opt/go/src/github.com/sendgrid/dx-automator/services/looker

CMD ["go", "run", "main.go"]