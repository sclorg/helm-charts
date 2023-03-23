# PostgreSQL helm chart

This repository contains helm chart for PostgreSQL image build and deployed on OpenShift.

For more information about helm charts see the offical [Helm Charts Documentation](https://helm.sh/).

You need to have access to a cluster for each operation with OpenShift 4, like deploying and testing.

## How to start with helm charts

The first of all download and Helm. Follow instructions mentioned [here](https://helm.sh/docs/intro/install/).

## How to work with PostgreSQL helm chart

Before deploying helm chart to OpenShift, you have to create a package.
This can be done by command:

```commandline
$ helm package ./
```

that will create a helm package named, `postgresql-persistent-v0.0.1.tgz` in this directory.

The next step is to upload Helm Chart to OpenShift. This is done by command:

```commandline
$ helm install postgresql-persistent postgresql-persistent-v0.0.1.tgz
```

## Troubleshooting
For case you need a computer readable output you can add to command mentioned above option `-o json`.

In case of installation failed for reason like:
```commandline
// Error: INSTALLATION FAILED: cannot re-use a name that is still in use
```
you have to uninstall previous PostgreSQL Helm Chart by command:

```commandline
$ helm uninstall postgresql-persistent
```


