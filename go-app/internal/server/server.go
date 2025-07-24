package server

import (
	"go-app/internal/handlers"
	"log"

	"github.com/gin-gonic/gin"
)

func StartServer() {
	r := gin.Default()

	r.GET("/", handlers.Home)
	r.GET("/health", handlers.HealthCheck)
	r.GET("/metrics", handlers.Metrics)
	r.GET("/error", handlers.Error)

	log.Println("Starting server on :8000")
	if err := r.Run(":8000"); err != nil {
		log.Fatalf("Could not start server: %s\n", err)
	}
}
