# Kubernetes Cluster Architecture

A zoned architecture diagram showing the full Kubernetes stack: external traffic
through a load balancer, the control plane (apiserver, etcd, controller manager,
scheduler), worker nodes with kubelet and pods, and persistent storage. Four
color-coded zones are drawn automatically around the nodes that belong to them.

![Kubernetes Cluster](./diagram.png)

## Prompt

```
Draw a Kubernetes cluster architecture diagram, top to bottom. Four zones:
EXTERNAL (Internet → Load Balancer), CONTROL PLANE (kube-apiserver hub connecting
to etcd, Controller Manager, Scheduler), WORKER NODES (kubelet managing Container
Runtime and three pods — App, Worker, Sidecar; kube-proxy with a dashed connection
to the App pod), STORAGE (PVC → PV → StorageClass chain, connected from the App
pod via a dashed line). Color code: blue for external, orange for control plane,
green for workers, purple for storage.
```

## Generation time

~5 seconds

## Files generated

| File | Description |
|------|-------------|
| `graph.json` | Declarative graph: nodes, edges, zones — no coordinates |
| `diagram.excalidraw` | Full Excalidraw JSON with dagre-computed positions |
| `diagram.svg` | Vector output |
| `diagram.png` | Raster output |

## Commands

```bash
node dagre-layout.js examples/k8s-cluster/graph.json \
  --output examples/k8s-cluster/diagram.excalidraw

excalidraw-agent-cli \
  --project examples/k8s-cluster/diagram.excalidraw \
  export png --output examples/k8s-cluster/diagram.png --overwrite

excalidraw-agent-cli \
  --project examples/k8s-cluster/diagram.excalidraw \
  export svg --output examples/k8s-cluster/diagram.svg --overwrite
```

## How zones work in graph.json

```json
"zones": [
  {
    "id": "cp",
    "label": "CONTROL PLANE",
    "labelColor": "#c2410c",
    "fill": "#ffedd5",
    "stroke": "#fdba74",
    "nodeIds": ["api", "etcd", "ctrlr", "sched"]
  }
]
```

Dagre-layout.js computes the bounding box of all nodes listed in `nodeIds`,
adds padding, and draws a background rectangle behind them with a zone label
in the top-left corner. No manual zone coordinates needed.
