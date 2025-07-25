package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func Redirect(c *gin.Context) {
	c.Header("Location", "/health")
	c.String(http.StatusFound, "Redirecting...")
}
