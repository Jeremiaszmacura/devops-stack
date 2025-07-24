package handlers

import (
	"net/http"
	"runtime"
	"time"

	"github.com/gin-gonic/gin"
)

func Metrics(c *gin.Context) {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)

	c.JSON(http.StatusOK, gin.H{
		"goroutines": runtime.NumGoroutine(),
		"memory": gin.H{
			"alloc_mb":       bToMb(m.Alloc),
			"total_alloc_mb": bToMb(m.TotalAlloc),
			"sys_mb":         bToMb(m.Sys),
		},
		"timestamp": time.Now().UTC().Format(time.RFC3339),
	})
}

func bToMb(b uint64) uint64 {
	return b / 1024 / 1024
}
