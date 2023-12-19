# SCLORG helm-charts

SCLORG Helm Charts is a repository hosting [Helm Charts](https://github.com/helm/helm) available out-of-the-box with [OpenShift](https://www.openshift.com/). It contains popular technologies, tools and services. Helm Charts on this repository can be provided by the community, by partners or Red Hat. 

Charts go through an automated Red Hat OpenShift certification workflow, which guarantees security compliance as well as best integration and experience with the platform.

## Structure of the repository

```
.
└── charts
    └── <centos|redhat>
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
$ helm package ./charts/<centos|redhat>/<chart-name>
```

Package can then be placed directly under `./charts/<centos|redhat>/<chart-name>` for example: `./charts/redhat/postgresql-persistent/`.

## Using Helm

Once this repository is available and configured, Helm Charts will be available in the [OpenShift Developer Perspective](https://docs.openshift.com/container-platform/latest/applications/application_life_cycle_management/odc-working-with-helm-charts-using-developer-perspective.html)

You can also use Helm CLI commands, please refere to [Using Helm Guide](https://helm.sh/docs/intro/using_helm/) for detailed instructions on how to use the Helm client.

## How to contribute to this repository

In case of Helm chart is related to CentOS, CentOS Stream 8, or CentOS Stream 9 then use [centos](charts/centos) directory.

In case of Helm chart is related to RHEL system then use [redhat](charts/redhat) directory.

As soon as your Helm chart follows directory structure as mentioned above, let's test it.

### General notes for Helm charts
Each helm chart name has to contain file OWNERS. E.g. [OWNERS](./charts/redhat/postgresql-imagestreams/OWNERS)

Each helm chart change, in [templates](./charts/redhat/postgresql-persistent/src/templates),
[Chart.yaml](./charts/redhat/postgresql-persistent/src/Chart.yaml),
[values.yaml](./charts/redhat/postgresql-persistent/src/values.yaml),
[values.schema.json](./charts/redhat/postgresql-persistent/src/values.schema.json),
or [OWNERS](./charts/redhat/postgresql-persistent/OWNERS) file
has to bump version.
Bump the version `appVersion` and `version` in `Chart.yaml` file.

```commandline
description: |-
  PostgreSQL database service, with persistent storage. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/postgresql-container/.

  NOTE: Scaling to more than one replica is not supported. You must have persistent volumes available in your cluster to use this template.
annotations:
  charts.openshift.io/name: Red Hat PostgreSQL database service, with persistent storage
apiVersion: v2
appVersion: 0.0.2
name: postgresql-persistent
tags: database,postgresql
sources:
  - https://github.com/sclorg/helm-charts
version: 0.0.2

```

### How to test Helm chart

As a prerequisite to testing Helm charts, you need to be connected to the OpenShift 4 cluster using the oc binary generated from the cluster itself.
To get access to OpenShift 4 cluster please ask phracek@redhat.com.

#### Create a Helm chart package

Before any testing proposes and deploying Helm chart to OpenShift cluster, you have to create a package using command:

```commandline
$ helm package <path_to_helm_chart>
```

E.g. Using postgresql-persistent Helm chart:

```commandline
$ helm package charts/redhat/postgresql-persistent/src
Successfully packaged chart and saved it to: <FULL_PATH_TO_CWD>/helm-charts/postgresql-persistent-0.0.1.tgz
```

#### Deploy Helm chart to OpenShift

You can deploy the Helm chart to the OpenShift cluster using command:

```commandline
$ helm install <helm_chart_name> <tarball_path>
```

E.g Using postgresql-persistent Helm chart:

```commandline
$ helm install postgresql-imagestreams postgresql-imagestreams-0.0.1.tgz
NAME: postgresql-imagestreams
LAST DEPLOYED: Tue Apr  4 10:29:33 2023
NAMESPACE: pgsql-13
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

To check if Helm chart is really deployed, run command:

```bash
helm list
```

Examples of the `helm list` output:

```commandline
$ helm list
NAME                      	NAMESPACE	REVISION	UPDATED                              	STATUS  	CHART                        	APP VERSION
postgresql-imagestreams  	pgsql-13 	1       	2023-04-04 10:29:33.878674 +0200 CEST	deployed	postgresql-imagestreams-0.0.1	0.0.1
postgresql-persistent     	pgsql-13 	1       	2023-03-28 16:59:56.498783 +0200 CEST	deployed	postgresql-persistent-0.0.1
```

#### How to test Helm chart

As soon as a Helm chart is deployed on OpenShift 4 cluster, let's test it.
Use the following command to test

```commandline
$ helm test <helm_chart_name> --logs
```

The output should be like:

```commandline
$ helm test postgresql-persistent --logs
NAME: postgresql-persistent
LAST DEPLOYED: Tue Mar 28 16:59:56 2023
NAMESPACE: pgsql-13
STATUS: deployed
REVISION: 1
TEST SUITE:     postgresql-persistent-connection-test
Last Started:   Tue Apr  4 10:31:44 2023
Last Completed: Tue Apr  4 10:31:52 2023
Phase:          Succeeded

POD LOGS: postgresql-persistent-connection-test
postgresql-testing:5432 - accepting connections
```

The end of the output shows, that PostgreSQL server accepts connections.

### How to verify Helm chart

As soon as a Helm chart is ready and tested let's verify it.

In case the Helm chart has already been merged,
use the following command to verify if all the required information is contained within the Helm chart.

```commandline
docker run --rm -i -e KUBECONFIG=/.kube/config -v "${HOME}/.kube":/.kube \
          "quay.io/redhat-certification/chart-verifier:latest" \
          verify \
          https://sclorg.github.io/helm-charts/<helm-chart-name>.tgz
```

Use the following command to verify if all the required information for local testing is contained within the Helm chart.

```commandline
docker run --rm -i -e KUBECONFIG=/.kube/config -v "${HOME}/.kube":/.kube \
          -v "<full_path_to_this_dir>":/helm-charts
          "quay.io/redhat-certification/chart-verifier:latest" \
          verify \
          /helm-charts/<helm-chart-name>.tgz
```

The output from commands mentioned above could look like:

```commandline
results:
    - check: v1.0/required-annotations-present
      type: Mandatory
      outcome: PASS
      reason: All required annotations present
    - check: v1.0/signature-is-valid
      type: Mandatory
      outcome: SKIPPED
      reason: 'Chart is not signed : Signature verification not required'
    - check: v1.0/chart-testing
      type: Mandatory
      outcome: FAIL
      reason: |-
        Chart Install failure: values don't meet the specifications of the schema(s) in the following chart(s):
        postgresql-persistent:
        enum items must be unique
[snipped]
    - check: v1.0/helm-lint
      type: Mandatory
      outcome: FAIL
      reason: |
        Helm lint has failed:  [INFO] Chart.yaml: icon is recommended
        [ERROR] values.yaml: enum items must be unique
        [ERROR] templates/: values don't meet the specifications of the schema(s) in the following chart(s):
        postgresql-persistent:
        enum items must be unique
[snipped]
    - check: v1.1/has-kubeversion
      type: Mandatory
      outcome: FAIL
      reason: Kubernetes version is not specified
    - check: v1.1/images-are-certified
      type: Mandatory
      outcome: FAIL
      reason: |-
        Failed to certify images : Failed to get images, error running helm template : values don't meet the specifications of the schema(s) in the following chart(s):
        postgresql-persistent:
        enum items must be unique
[snipped]
    - check: v1.0/contains-values
      type: Mandatory
      outcome: PASS
      reason: Values file exist
    - check: v1.0/not-contains-crds
      type: Mandatory
      outcome: PASS
      reason: Chart does not contain CRDs
```

Address all issues detected by chart-verifier.

## Troubleshooting

Before any questions, see [https://github.com/openshift-helm-charts/charts/blob/main/docs/README.md](https://github.com/openshift-helm-charts/charts/blob/main/docs/README.md).
