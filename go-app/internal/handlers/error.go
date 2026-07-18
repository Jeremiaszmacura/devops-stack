package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// Error returns a simulated 500 response for testing error monitoring.
func Error(c *gin.Context) {
	c.JSON(http.StatusInternalServerError, gin.H{
		"error":     "This is a simulated error endpoint",
		"code":      500,
		"timestamp": time.Now().UTC().Format(time.RFC3339),
		"service":   "go-app",
	})
}
