# AWS CDK Datadog Resources

[![npm version](https://badge.fury.io/js/%40nomadblacky%2Fcdk-datadog-resources.svg)](https://badge.fury.io/js/%40nomadblacky%2Fcdk-datadog-resources)

An AWS CDK construct library that wrapped [DataDog/datadog-cloudformation-resources](https://github.com/DataDog/datadog-cloudformation-resources).

## Requirements

Before use this library, [register datadog-cloudformation-resources to your AWS account.](https://github.com/DataDog/datadog-cloudformation-resources#datadog-aws-cloudformation)

You need to register the correct version listed in `Supported Resources`.

## Supported CDK Languages

* TypeScript
* Python
* ~~Java~~ Sorry, there is a problem with the release. ([#22](https://github.com/NomadBlacky/cdk-datadog-resources/issues/22))

## Supported Resources

| Supported? | Resource                | Datadog CF Resource Name         | Description                                              | Datadog CF Version |
| :--------: | ----------------------- | -------------------------------- | -------------------------------------------------------- | ------------------ |
|     ✅     | Dashboards              | `Datadog::Dashboards::Dashboard` | [Create, update, and delete Datadog dashboards.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-dashboards-dashboard-handler)      | [1.0.0](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-dashboards-dashboard-handler/CHANGELOG.md#100--2021-02-16)         |
|            | Datadog-AWS integration | `Datadog::Integrations::AWS`     | [Manage your Datadog-Amazon Web Service integration.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-integrations-aws-handler) | N/A                |
|     ✅     | Monitors                | `Datadog::Monitors::Monitor`     | [Create, update, and delete Datadog monitors.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-monitors-monitor-handler)        | [3.0.0](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-monitors-monitor-handler/CHANGELOG.md#300--2021-02-16)         |
|     ✅     | Downtimes               | `Datadog::Monitors::Downtime`    | [Enable or disable downtimes for your monitors.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-monitors-downtime-handler)      | [2.0.0](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-monitors-downtime-handler/CHANGELOG.md#200--2021-02-16)         |
|     ✅     | Users                   | `Datadog::IAM::User`             | [Create and manage Datadog users.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-iam-user-handler)                    | [1.2.0](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-iam-user-handler/CHANGELOG.md#120--2021-02-16)         |

## Installation

TypeScript

```shell
npm install @nomadblacky/cdk-datadog-resources
```

Python

```shell
pip install cdk-datadog-resources
```

Java

```xml
<dependency>
    <groupId>dev.nomadblacky</groupId>
    <artifactId>cdk-datadog-resources</artifactId>
    <version>x.y.z</version>
</dependency>
```

## Usage

Belows are examples of TypeScript.

### Dashboards

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import fs as fs
from nomadblacky.cdk_datadog_resources import DatadogDashboard

DatadogDashboard(your_stack, "TestDashboard",
    datadog_credentials={
        "api_key": process.env.DATADOG_API_KEY,
        "application_key": process.env.DATADOG_APP_KEY
    },
    dashboard_definition=fs.read_file_sync(f"{__dirname}/path/to/your/dashboard-definition.json").to_string()
)
```

### Monitors

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from nomadblacky.cdk_datadog_resources import DatadogMonitor

DatadogMonitor(your_stack, "TestMonitor",
    datadog_credentials={
        "api_key": process.env.DATADOG_API_KEY,
        "application_key": process.env.DATADOG_APP_KEY
    },
    query="avg(last_1h):sum:system.cpu.system{host:host0} > 100",
    type=MonitorType.QueryAlert,
    name="Test Monitor",
    options={
        "thresholds": {
            "critical": 100,
            "warning": 80,
            "o_k": 90
        },
        "notify_no_data": True,
        "evaluation_delay": 60
    }
)
```

### Downtimes

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from nomadblacky.cdk_datadog_resources import DatadogDowntime

DatadogDowntime(stack, "TestMonitor",
    datadog_credentials={
        "api_key": "DATADOG_API_KEY",
        "application_key": "DATADOG_APP_KEY"
    },
    scope=["host:myserver", "service:myservice"],
    start=1624542715,
    end=1624546321
)
```

### Users

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from nomadblacky.cdk_datadog_resources import DatadogIAMUser

DatadogIAMUser(stack, "TestUser",
    datadog_credentials={
        "api_key": "DATADOG_API_KEY",
        "application_key": "DATADOG_APP_KEY"
    },
    email="jane.doe@example.com",
    name="name_example",
    handle="title_example",
    disabled=False
)
```
