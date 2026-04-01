FROM golang:1.20 AS builder

WORKDIR /app

COPY go.mod ./
COPY . .
RUN go mod tidy

RUN go build -o go-app ./cmd/main.go

FROM gcr.io/distroless/base

COPY --from=builder /app/go-app /go-app

EXPOSE 8080

CMD ["/go-app"]