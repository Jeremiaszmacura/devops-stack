package server

import (
	"go-app/internal/handlers"
	"go-app/internal/metrics"
	"log"

	"github.com/gin-gonic/gin"
)

func StartServer() error {
	r := gin.Default()
	r.Use(metrics.PrometheusMiddleware())

	r.GET("/", handlers.Home)
	r.GET("/health", handlers.HealthCheck)
	r.GET("/metrics", handlers.Metrics)
	r.GET("/error", handlers.Error)
	r.GET("/redirect", handlers.Redirect)

	log.Println("Starting Go server on :8080")
	return r.Run(":8080")
}
