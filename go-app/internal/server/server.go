package server

import (
	"fmt"
	"log"

	"go-app/internal/appmetrics"
	"go-app/internal/handlers"

	"github.com/gin-gonic/gin"
)

func StartServer() error {
	router := gin.Default()                       // Initialize default Gin router (includes Logger and Recovery middleware)
	router.Use(appmetrics.PrometheusMiddleware()) // Custom middleware for Prometheus metrics

	router.GET("/", handlers.Home)
	router.GET("/health", handlers.HealthCheck)
	router.GET("/metrics", handlers.Metrics)
	router.GET("/error", handlers.Error)
	router.GET("/redirect", handlers.Redirect)

	log.Println("Starting Go server on :8080")
	if err := router.Run(":8080"); err != nil {
		return fmt.Errorf("failed to start server: %w", err)
	}
	return nil
}
