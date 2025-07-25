package main

import (
	"go-app/internal/server"
	"log"
)

func main() {
	log.Println("Starting Go application...")

	if err := server.StartServer(); err != nil {
		log.Fatalf("Could not start server: %v", err)
	}
}
