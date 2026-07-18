package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// Redirect responds with a 302 redirect to the /health endpoint.
func Redirect(c *gin.Context) {
	c.Redirect(http.StatusFound, "/health")
}
