package handlers

import (
	"errors"
	"net/http"

	"go-app/internal/vaultclient"

	"github.com/gin-gonic/gin"
)

// SecretsHandler serves the /secret endpoints backed by Vault.
type SecretsHandler struct {
	vault *vaultclient.Client
}

// NewSecretsHandler returns a SecretsHandler storing secrets through vault.
func NewSecretsHandler(vault *vaultclient.Client) *SecretsHandler {
	return &SecretsHandler{vault: vault}
}

// secretRequest is the request body for storing a secret.
type secretRequest struct {
	Key   string `json:"key" binding:"required"`
	Value string `json:"value" binding:"required"`
}

// Write stores the secret from the request body in Vault.
func (h *SecretsHandler) Write(c *gin.Context) {
	var req secretRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "key and value are required"})
		return
	}

	if err := h.vault.WriteSecret(c.Request.Context(), req.Key, req.Value); err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "vault request failed"})
		return
	}
	c.JSON(http.StatusCreated, gin.H{"key": req.Key, "status": "stored"})
}

// Read returns the secret stored in Vault under the key path parameter.
func (h *SecretsHandler) Read(c *gin.Context) {
	key := c.Param("key")

	value, err := h.vault.ReadSecret(c.Request.Context(), key)
	if errors.Is(err, vaultclient.ErrSecretNotFound) {
		c.JSON(http.StatusNotFound, gin.H{"error": "secret not found"})
		return
	}
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "vault request failed"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"key": key, "value": value})
}
