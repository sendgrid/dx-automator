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

#Twilio Monitors
resource "datadog_monitor" "time_to_contact_issues_twilio" {
  name    = "Mean time to contact for Issues for Twilio Org"
  type    = "metric alert"
  message = "@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Mean time to contact for Issues for Twilio org= {{value}}. We are in breach of our SLO (<=30 days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to contact for Issues for Twilio org= {{value}}. Our SLA threshold is <= 30 days. {{override_priority 'P3'}} {{/is_warning}} ```"
  query   = "sum(last_5m):max:library.time_to_contact.mean{org:twilio} >= 30"

  monitor_thresholds {
    warning  = var.time_to_contact_issues_warning
    critical = var.time_to_contact_issues_critical
  }

  tags = ["owner:developer_experience", "team:dev-Interfaces"]
}

resource "datadog_monitor" "time_to_contact_PRs_twilio" {
  name    = "Mean time to contact for PRs for Twilio Org"
  type    = "metric alert"
  message = "@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Mean time to contact for PRs for Twilio org= {{value}}. We are in breach of our SLO (<=10 days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to contact for PRs for Twilio org= {{value}}. Our SLA threshold is <= 10 days. {{override_priority 'P3'}} {{/is_warning}} ```"
  query   = "sum(last_5m):max:library.time_to_contact_pr.mean{org:twilio} >= 10"

  monitor_thresholds {
    warning  = var.time_to_contact_PRs_warning
    critical = var.time_to_contact_PRs_critical
  }

  tags = ["owner:developer_experience", "team:dev-Interfaces"]
}

resource "datadog_monitor" "time_to_resolve_issue_twilio" {
  name    = "Time to resolve issues for Twilio Org"
  type    = "metric alert"
  message = "@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Mean time to contact for Issues for SendGrid org= {{value}}. We are in breach of our SLO (<=30 days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to contact for Issues for SendGrid org= {{value}}. Our SLA threshold is <= 30 days. {{override_priority 'P3'}} {{/is_warning}} ```"
  query   = "sum(last_5m):max:library.time_to_close.mean{org:twilio} >= 180"

  monitor_thresholds {
    warning  = var.time_to_resolve_issue_warning
    critical = var.time_to_resolve_issue_critical
  }

  tags = ["owner:developer_experience", "team:dev-Interfaces"]
}

resource "datadog_monitor" "open_issue_count_twilio" {
  name    = "Open Issues Count for Twilio Org"
  type    = "metric alert"
  message = "@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Open issues count for Twilio org= {{value}}. We are in breach of our SLO (<=84). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Open issues count for Twilio org= {{value}}. Our SLA threshold is <= 84. {{override_priority 'P3'}} {{/is_warning}}```"
  query   = "sum(last_5m):sum:library.issue_count.count{org:twilio} >= 84"

  monitor_thresholds {
    warning  = var.open_issue_count_warning
    critical = var.open_issue_count_twilio_critical
  }

  tags = ["owner:developer_experience", "team:dev-Interfaces"]
}
resource "datadog_monitor" "GH_helper_library_release_is_due" {
  name    = "Github Helper Library Release is due"
  type    = "metric alert"
  message = "@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Average count of releases per repo= {{value}}. We are in breach of our SLO (at least 2 releases per repo within 30 days). {{override_priority 'P1'}} {{/is_alert}}```"
  query   = "sum(last_1mo):avg:library.release.count{*}.as_count() < 2"

  monitor_thresholds {
    critical = 2
  }

  tags = ["owner:developer_experience", "team:dev-Interfaces"]
}

#Sendgrid Monitors
resource "datadog_monitor" "time_to_contact_issues_sendgrid" {
  name    = "Mean time to contact for Issues for Sendgrid Org"
  type    = "metric alert"
  message = "@slack-Twilio-alerts-dev-interfaces ``` {{#is_alert}} ALERT! Mean time to contact for Issues for SendGrid org= {{value}}. We are in breach of our SLO (<=30 days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to contact for Issues for SendGrid org= {{value}}. Our SLA threshold is <= 30 days. {{override_priority 'P3'}} {{/is_warning}}```"
  query   = "sum(last_5m):max:library.time_to_contact.mean{org:sendgrid} >= 30"

  monitor_thresholds {
    warning  = var.time_to_contact_issues_warning
    critical = var.time_to_contact_issues_critical
  }

  tags = ["owner:developer_experience", "team:dev-Interfaces"]
}

resource "datadog_monitor" "time_to_contact_PRs_sendgrid" {
  name    = "Mean time to contact for PRs for SendGrid Org"
  type    = "metric alert"
  message = "@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Mean time to contact for PRs for SendGrid org= {{value}}. We are in breach of our SLO (<=10 days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to contact for PRs for SendGrid org= {{value}}. Our SLA threshold is <= 10 days. {{override_priority 'P3'}} {{/is_warning}}```"
  query   = "sum(last_5m):max:library.time_to_contact_pr.mean{org:sendgrid} >= 10"

  monitor_thresholds {
    warning  = var.time_to_contact_PRs_warning
    critical = var.time_to_contact_PRs_critical
  }

  tags = ["owner:developer_experience", "team:dev-Interfaces"]
}

resource "datadog_monitor" "time_to_resolve_PRs_sendgrid" {
  name    = "Mean time to resolve issues for SendGrid Org"
  type    = "metric alert"
  message = "@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Mean time to resolve issues for SendGrid org= {{value}}. We are in breach of our SLO (<=180 days). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Mean time to resolve issues for SendGrid org= {{value}}. Our SLA threshold is <= 180 days. {{override_priority 'P3'}} {{/is_warning}}```"
  query   = "sum(last_5m):max:library.time_to_close.mean{org:sendgrid} >= 180"

  monitor_thresholds {
    warning  = var.time_to_resolve_issue_warning
    critical = var.time_to_resolve_issue_critical
  }

  tags = ["owner:developer_experience", "team:dev-Interfaces"]
}

resource "datadog_monitor" "open_issue_count_sendgrid" {
  name    = "Open Issues Count for SendGrid Org"
  type    = "metric alert"
  message = "@slack-Twilio-alerts-dev-interfaces ```{{#is_alert}} ALERT! Open issues count for SendGrid org= {{value}}. We are in breach of our SLO (<=80). {{override_priority 'P1'}} {{/is_alert}} {{#is_warning}} WARNING! Open issues count for SendGrid org= {{value}}. Our SLA threshold is <= 80. {{override_priority 'P3'}} {{/is_warning}}```"
  query   = "sum(last_5m):sum:library.issue_count.count{org:sendgrid} >= 80"

  monitor_thresholds {
    warning  = var.open_issue_count_warning
    critical = var.open_issue_count_sendgrid_critical
  }

  tags = ["owner:developer_experience", "team:dev-Interfaces"]
}
