# Prometheus

This directory contains the configuration and setup files for Prometheus monitoring in the Kubernetes cluster.

## Monitor Kubernetes Cluster

To monitor the Kubernetes cluster, Prometheus needs node exporterts. Node exporters are deamonset kind of deployments that run on each node in the cluster. They collect metrics about the node's hardware and operating system, which Prometheus can scrape.

## Monitor Custom Applications

To minitor custom applications, you need to expose metrics in a format that Prometheus can scrape. This typically involves adding an endpoint (ex.: `/metrics`) to your application that serves metrics in the Prometheus format.