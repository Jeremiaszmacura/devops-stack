package main

import (
	"log"

	"go-app/internal/server"
)

func main() {
	// Start the server
	if err := server.StartServer(); err != nil {
		log.Fatalf("Could not start server: %v", err)
	}
}
