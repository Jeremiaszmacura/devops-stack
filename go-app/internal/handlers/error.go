package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func Error(c *gin.Context) {
	c.JSON(http.StatusInternalServerError, gin.H{
		"error":     "This is a simulated error endpoint",
		"code":      "500",
		"timestamp": time.Now().UTC().Format(time.RFC3339),
	})
}
