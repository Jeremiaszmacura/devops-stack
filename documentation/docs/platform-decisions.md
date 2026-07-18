# Platform Engineering Decisions

This page records the architectural decisions for the platform engineering,
related to cluster configuration, deployment and management.

## Deployments

* Cluster wide configuration and management of the cluster are defined in infra directory.
It contains Resources like ClusterRole, ClusterRoleBinding, ServiceAccount, RBAC, etc.

* K8s Resources like Deployments, StatefulSets, and DaemonSets are placed in the
`k8s/` directory of the component/service that owns them.

## Rules for placing K8s resources

### ServiceAccounts

- **Application-specific:** if the ServiceAccount belongs to a specific
  microservice/application, place it in the Application/Environment Repository —
  the owning component's `k8s/` directory, next to that component's Deployment.
- **Cluster-wide/Infrastructure:** if the ServiceAccount is for cluster-wide
  tools (e.g. monitoring, logging, ingress), place it in the Cluster
  Admin/Infrastructure Repository — `monitoring/<tool>/k8s/` for the monitoring
  stack, or the cluster bootstrap for controllers installed by
  `recreate-cluster.sh`.
- **Strict constraint:** never mix application-level ServiceAccounts into the
  global cluster admin repository. An application's identity is part of that
  application; keeping it in the cluster admin repository hides who owns it and
  couples application changes to cluster-admin changes.
