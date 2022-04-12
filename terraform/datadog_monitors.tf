terraform {
  required_providers {
    datadog = {
      source  = "DataDog/datadog"
      version = "3.10.0"
    }
  }
}

#Monitor threshold values
variable "time_to_contact_issues_warning" {
  type    = number
  default = 5
}
variable "time_to_contact_issues_critical" {
  type    = number
  default = 30
}
variable "time_to_contact_PRs_warning" {
  type    = number
  default = 5
}
variable "time_to_contact_PRs_critical" {
  type    = number
  default = 10
}
variable "time_to_resolve_issue_warning" {
  type    = number
  default = 30
}
variable "time_to_resolve_issue_critical" {
  type    = number
  default = 180
}
variable "open_issue_count_warning" {
  type    = number
  default = 50
}
variable "open_issue_count_twilio_critical" {
  type    = number
  default = 84
}
variable "open_issue_count_sendgrid_critical" {
  type    = number
  default = 80
}
variable "GH_helper_library_release_critical" {
  type    = number
  default = 2
}


#Twilio Monitors
resource "datadog_monitor" "time_to_contact_issues_twilio" {
  name    = "Mean time to contact for Issues for Twilio Org [TERRAFORM]"
  type    = "metric alert"
  message = format("@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Mean time to contact for Issues for Twilio org= {{value}}. We are in breach of our SLO (<= %s days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to contact for Issues for Twilio org= {{value}}. Our SLA threshold is <= %s days. {{override_priority 'P3'}} {{/is_warning}} ```", var.time_to_contact_issues_critical, var.time_to_contact_issues_critical)
  query   = format("sum(last_5m):max:library.time_to_contact.mean{org:twilio} >= %s", var.time_to_contact_issues_critical)

  monitor_thresholds {
    warning  = var.time_to_contact_issues_warning
    critical = var.time_to_contact_issues_critical
  }

  tags = ["owner:developer_experience", "team:dev_interfaces"]
}

resource "datadog_monitor" "time_to_contact_PRs_twilio" {
  name    = "Mean time to contact for PRs for Twilio Org [TERRAFORM]"
  type    = "metric alert"
  message = format("@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Mean time to contact for PRs for Twilio org= {{value}}. We are in breach of our SLO (<= %s days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to contact for PRs for Twilio org= {{value}}. Our SLA threshold is <= %s days. {{override_priority 'P3'}} {{/is_warning}} ```", var.time_to_contact_PRs_critical, var.time_to_contact_PRs_critical)
  query   = format("sum(last_5m):max:library.time_to_contact_pr.mean{org:twilio} >= %s", var.time_to_contact_PRs_critical)

  monitor_thresholds {
    warning  = var.time_to_contact_PRs_warning
    critical = var.time_to_contact_PRs_critical
  }

  tags = ["owner:developer_experience", "team:dev_interfaces"]
}

resource "datadog_monitor" "time_to_resolve_issue_twilio" {
  name    = "Time to resolve issues for Twilio Org [TERRAFORM]"
  type    = "metric alert"
  message = format("```{{#is_alert}} ALERT! Mean time to resolve issues for Twilio org= {{value}}. We are in breach of our SLO (<= %s days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to resolve issues for Twilio org= {{value}}. Our SLA threshold is <= %s days. {{override_priority 'P3'}} {{/is_warning}} ```", var.time_to_resolve_issue_critical, var.time_to_resolve_issue_critical)
  query   = format("sum(last_5m):max:library.time_to_close.mean{org:twilio} >= %s", var.time_to_resolve_issue_critical)

  monitor_thresholds {
    warning  = var.time_to_resolve_issue_warning
    critical = var.time_to_resolve_issue_critical
  }

  tags = ["owner:developer_experience", "team:dev_interfaces"]
}

resource "datadog_monitor" "open_issue_count_twilio" {
  name    = "Open Issues Count for Twilio Org [TERRAFORM]"
  type    = "metric alert"
  message = format("@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Open issues count for Twilio org= {{value}}. We are in breach of our SLO (<= %s). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Open issues count for Twilio org= {{value}}. Our SLA threshold is <= %s. {{override_priority 'P3'}} {{/is_warning}}```", var.open_issue_count_twilio_critical, var.open_issue_count_twilio_critical)
  query   = format("sum(last_5m):sum:library.issue_count.count{org:twilio} >= %s", var.open_issue_count_twilio_critical)

  monitor_thresholds {
    warning  = var.open_issue_count_warning
    critical = var.open_issue_count_twilio_critical
  }

  tags = ["owner:developer_experience", "team:dev_interfaces"]
}
resource "datadog_monitor" "GH_helper_library_release_is_due" {
  name    = "Github Helper Library Release is due [TERRAFORM]"
  type    = "metric alert"
  message = format("@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Average count of releases per repo= {{value}}. We are in breach of our SLO (at least %s releases per repo within 30 days). {{override_priority 'P1'}} {{/is_alert}}```", var.GH_helper_library_release_critical)
  query   = format("sum(last_1mo):avg:library.release.count{*}.as_count() < %s", var.GH_helper_library_release_critical)

  monitor_thresholds {
    critical = var.GH_helper_library_release_critical
  }

  tags = ["owner:developer_experience", "team:dev_interfaces"]
}

#SendGrid Monitors
resource "datadog_monitor" "time_to_contact_issues_sendgrid" {
  name    = "Mean time to contact for Issues for Sendgrid Org [TERRAFORM]"
  type    = "metric alert"
  message = format("@slack-Twilio-alerts-dev-interfaces ``` {{#is_alert}} ALERT! Mean time to contact for Issues for SendGrid org= {{value}}. We are in breach of our SLO (<= %s days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to contact for Issues for SendGrid org= {{value}}. Our SLA threshold is <= %s days. {{override_priority 'P3'}} {{/is_warning}}```", var.time_to_contact_issues_critical, var.time_to_contact_issues_critical)
  query   = format("sum(last_5m):max:library.time_to_contact.mean{org:sendgrid} >= %s", var.time_to_contact_issues_critical)

  monitor_thresholds {
    warning  = var.time_to_contact_issues_warning
    critical = var.time_to_contact_issues_critical
  }

  tags = ["owner:developer_experience", "team:dev_interfaces"]
}

resource "datadog_monitor" "time_to_contact_PRs_sendgrid" {
  name    = "Mean time to contact for PRs for SendGrid Org [TERRAFORM]"
  type    = "metric alert"
  message = format("@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Mean time to contact for PRs for SendGrid org= {{value}}. We are in breach of our SLO (<= %s days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to contact for PRs for SendGrid org= {{value}}. Our SLA threshold is <= %s days. {{override_priority 'P3'}} {{/is_warning}}```", var.time_to_contact_PRs_critical, var.time_to_contact_PRs_critical)
  query   = format("sum(last_5m):max:library.time_to_contact_pr.mean{org:sendgrid} >= %s", var.time_to_contact_PRs_critical)

  monitor_thresholds {
    warning  = var.time_to_contact_PRs_warning
    critical = var.time_to_contact_PRs_critical
  }

  tags = ["owner:developer_experience", "team:dev_interfaces"]
}

resource "datadog_monitor" "time_to_resolve_PRs_sendgrid" {
  name    = "Mean time to resolve issues for SendGrid Org [TERRAFORM]"
  type    = "metric alert"
  message = format("@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Mean time to resolve issues for SendGrid org= {{value}}. We are in breach of our SLO (<= %s days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to resolve issues for SendGrid org= {{value}}. Our SLA threshold is <= %s days. {{override_priority 'P3'}} {{/is_warning}}```", var.time_to_resolve_issue_critical, var.time_to_resolve_issue_critical)
  query   = format("sum(last_5m):max:library.time_to_close.mean{org:sendgrid} >= %s", var.time_to_resolve_issue_critical)

  monitor_thresholds {
    warning  = var.time_to_resolve_issue_warning
    critical = var.time_to_resolve_issue_critical
  }

  tags = ["owner:developer_experience", "team:dev_interfaces"]
}

resource "datadog_monitor" "open_issue_count_sendgrid" {
  name    = "Open Issues Count for SendGrid Org [TERRAFORM]"
  type    = "metric alert"
  message = format("@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Open issues count for SendGrid org= {{value}}. We are in breach of our SLO (<= %s). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Open issues count for SendGrid org= {{value}}. Our SLA threshold is <= %s. {{override_priority 'P3'}} {{/is_warning}}```", var.open_issue_count_sendgrid_critical, var.open_issue_count_sendgrid_critical)
  query   = format("sum(last_5m):sum:library.issue_count.count{org:sendgrid} >= %s", var.open_issue_count_sendgrid_critical)

  monitor_thresholds {
    warning  = var.open_issue_count_warning
    critical = var.open_issue_count_sendgrid_critical
  }

  tags = ["owner:developer_experience", "team:dev_interfaces"]
}
