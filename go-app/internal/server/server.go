package server

import (
	"go-app/internal/handlers"
	"go-app/internal/metrics"
	"log"

	"github.com/gin-gonic/gin"
)

func StartServer() error {
	router := gin.Default()                    // Initialize default Gin router (includes Logger and Recovery middleware)
	router.Use(metrics.PrometheusMiddleware()) // Custom middleware for Prometheus metrics

	router.GET("/", handlers.Home)
	router.GET("/health", handlers.HealthCheck)
	router.GET("/metrics", handlers.Metrics)
	router.GET("/error", handlers.Error)
	router.GET("/redirect", handlers.Redirect)

	log.Println("Starting Go server on :8080")
	return router.Run(":8080")
}
