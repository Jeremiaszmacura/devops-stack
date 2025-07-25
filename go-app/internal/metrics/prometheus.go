package metrics

import (
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (
	// Main application metrics
	RequestCount = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "http_requests_total",
			Help: "Total number of HTTP requests",
		},
		[]string{"method", "endpoint", "status_code"},
	)

	RequestDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "http_request_duration_seconds",
			Help:    "HTTP request duration in seconds",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"method", "endpoint"},
	)

	ResponseStatus = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "http_responses_by_status_total",
			Help: "HTTP responses by status code",
		},
		[]string{"status_class"},
	)

	// Separate metric for monitoring requests
	MonitoringRequests = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "monitoring_requests_total",
			Help: "Total number of monitoring/metrics requests",
		},
		[]string{"endpoint", "user_agent"},
	)
)

// PrometheusMiddleware tracks HTTP metrics
func PrometheusMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()

		// Process request
		c.Next()

		// Calculate duration
		duration := time.Since(start).Seconds()

		// Extract request info
		endpoint := c.FullPath()
		if endpoint == "" {
			endpoint = c.Request.URL.Path
		}
		method := c.Request.Method
		statusCode := strconv.Itoa(c.Writer.Status())
		userAgent := c.GetHeader("User-Agent")

		// Track metrics differently for app vs monitoring endpoints
		if endpoint != "/metrics" && endpoint != "/health" {
			// Application metrics
			RequestCount.WithLabelValues(method, endpoint, statusCode).Inc()
			RequestDuration.WithLabelValues(method, endpoint).Observe(duration)

			// Status class (2XX, 3XX, 4XX, 5XX)
			statusClass := string(statusCode[0]) + "XX"
			ResponseStatus.WithLabelValues(statusClass).Inc()
		}

		// Separate tracking for monitoring endpoints
		if endpoint == "/metrics" || endpoint == "/health" {
			// Extract simplified user agent (e.g., "Prometheus" from "Prometheus/2.x.x")
			simplifiedUA := userAgent
			if strings.Contains(userAgent, "/") {
				simplifiedUA = strings.Split(userAgent, "/")[0]
			}
			if simplifiedUA == "" {
				simplifiedUA = "unknown"
			}
			MonitoringRequests.WithLabelValues(endpoint, simplifiedUA).Inc()
		}
	}
}
