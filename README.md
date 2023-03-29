# SCLORG helm-charts

SCLORG Helm Charts is a repository hosting [Helm Charts](https://github.com/helm/helm) available out-of-the-box with [OpenShift](https://www.openshift.com/). It contains popular technologies, tools and services. Helm Charts on this repository can be provided by the community, by partners or Red Hat. 

Charts go through an automated Red Hat OpenShift certification workflow, which guarantees security compliance as well as best integration and experience with the platform.

## Structure of the repository

```
.
└── charts
    └── sclorg
        └── <chart-name>
            └── src
                ├── Chart.yaml
                ├── README.md
                ├── templates
                │   ├── deployment.yaml
                │   ├── _helpers.tpl
                │   ├── hpa.yaml
                │   ├── ingress.yaml
                │   ├── NOTES.txt
                │   ├── serviceaccount.yaml
                │   ├── service.yaml
                │   └── tests
                │       └── test-connection.yaml
                ├── values.schema.json
                └── values.yaml
```

The chart can also be packaged using the following command:

```bash
$ helm package ./charts/sclorg/<chart-name>
```

Package can then be placed directly under `./charts/sclorg/<chart-name>` for example: `./charts/sclorg/postgresql-persistent/`.

### Contributing Helm Charts 

Interested in getting your helm charts Red Hat OpenShift certified? read the [certification documention](https://github.com/sclorg/helm-charts/pulls)

## Installation

```bash
$ helm repo add sclorg-helm-charts https://charts.openshift.io/
```

## Using Helm

Once this repository is available and configured, Helm Charts will be available in the [OpenShift Developer Perspective](https://docs.openshift.com/container-platform/latest/applications/application_life_cycle_management/odc-working-with-helm-charts-using-developer-perspective.html)

You can also use Helm CLI commands, please refere to [Using Helm Guide](https://helm.sh/docs/intro/using_helm/) for detailed instructions on how to use the Helm client.
