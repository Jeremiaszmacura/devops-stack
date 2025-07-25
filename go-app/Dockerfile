FROM golang:1.20 AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o go-app ./cmd/main.go

FROM gcr.io/distroless/base

COPY --from=builder /app/go-app /go-app

EXPOSE 8080

CMD ["/go-app"]