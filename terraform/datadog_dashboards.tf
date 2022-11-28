locals {
  monitor_ids = {
    open_issue_count_twilio = "68688791"
    mean_time_to_resolve_issues_twilio = "68688785"
    mean_time_to_contact_issues_twilio = "68688790"
    mean_time_to_contact_prs_twilio = "68688784"
    max_time_to_contact_issue_twilio = "89025823"
    max_time_to_contact_prs_twilio = "89025826"
    max_time_to_resolve_issues_twilio = "89025822"
  }
}

resource "datadog_dashboard" "ordered_dashboard" {
  title        = "Developer Interfaces Metrics [TERRAFORM]"
  description  = "This dashboard includes metrics for the Developer Tools Team's metrics for the products we own. Reach out to #help-dev-interfaces with any questions on Slack."
  layout_type  = "ordered"

  widget {
    group_definition {
      layout_type = "ordered"
      title       = "Coverage Metrics"
      show_title = true
      background_color = "vivid_blue"

      widget {
        toplist_definition {
          title = "Twilio Line Coverage"  
          request {
            formula {
              formula_expression = "(query1 - query2) / query1 * 100"
              limit {
                count = 500
                order = "desc"
              }
            }
            conditional_formats {
              palette = "white_on_yellow"
              value = "80"
              comparator = "<"
            }
            conditional_formats {
              palette = "white_on_red"
              value = "50"
              comparator = "<"
            }
            conditional_formats {
              palette = "white_on_green"
              value = "80"
              comparator = ">="
            }
            query {
              metric_query {
                  data_source = "metrics"
                  query       = "avg:sonar_cloud.measures.lines_to_cover{org:twilio,pre-release:false} by {repo}"
                  name        = "query1"
                  aggregator  = "last"
              }
            }
            query {
              metric_query {
                  data_source = "metrics"
                  query      = "avg:sonar_cloud.measures.uncovered_lines{org:twilio,pre-release:false} by {repo}"
                  name       = "query2"
                  aggregator = "last"
              }
            }
          }
        }
      }

      widget {
        toplist_definition {
          title = "Twilio Branch Coverage"  
          request {
            formula {
              formula_expression = "query1"
              limit {
                count = 500
                order = "desc"
              }
            }
            conditional_formats {
              palette = "white_on_yellow"
              value = "80"
              comparator = "<"
            }
            conditional_formats {
              palette = "white_on_red"
              value = "50"
              comparator = "<"
            }
            conditional_formats {
              palette = "white_on_green"
              value = "80"
              comparator = ">="
            }
            query {
              metric_query {
                  data_source = "metrics"
                  query       = "avg:sonar_cloud.measures.branch_coverage{org:twilio,pre-release:false} by {repo}"
                  name        = "query1"
                  aggregator  = "last"
              }
            }
          }
        }
      }

      widget {
        toplist_definition {
          title = "Twilio Release Candidate Line Coverage"  
          request {
            formula {
              formula_expression = "(query1 - query2) / query1 * 100"
              limit {
                count = 500
                order = "desc"
              }
            }
            conditional_formats {
              palette = "white_on_yellow"
              value = "80"
              comparator = "<"
            }
            conditional_formats {
              palette = "white_on_red"
              value = "50"
              comparator = "<"
            }
            conditional_formats {
              palette = "white_on_green"
              value = "80"
              comparator = ">="
            }
            query {
              metric_query {
                  data_source = "metrics"
                  query       = "avg:sonar_cloud.measures.lines_to_cover{org:twilio,pre-release:true} by {repo}"
                  name        = "query1"
                  aggregator  = "last"
              }
            }
            query {
              metric_query {
                  data_source = "metrics"
                  query      = "avg:sonar_cloud.measures.uncovered_lines{org:twilio,pre-release:true} by {repo}"
                  name       = "query2"
                  aggregator = "last"
              }
            }
          }
        }
      }

      widget {
        toplist_definition {
          title = "Twilio Release Candidate Branch Coverage"  
          request {
            formula {
              formula_expression = "query1"
              limit {
                count = 500
                order = "desc"
              }
            }
            conditional_formats {
              palette = "white_on_yellow"
              value = "80"
              comparator = "<"
            }
            conditional_formats {
              palette = "white_on_red"
              value = "50"
              comparator = "<"
            }
            conditional_formats {
              palette = "white_on_green"
              value = "80"
              comparator = ">="
            }
            query {
              metric_query {
                  data_source = "metrics"
                  query       = "avg:sonar_cloud.measures.branch_coverage{org:twilio,pre-release:true} by {repo}"
                  name        = "query1"
                  aggregator  = "last"
              }
            }
          }
        }
      }
    }
  }

  widget {
    group_definition {
      layout_type = "ordered"
      title       = "SLO Metrics"
      show_title = true
      background_color = "vivid_pink"

      widget {
        alert_graph_definition {
          alert_id  = local.monitor_ids.open_issue_count_twilio
          viz_type  = "timeseries"
          title     = "Open Issues Count for Twilio Org (SLO <= 84)"
        }
      }

      widget {
        alert_graph_definition {
          alert_id  = local.monitor_ids.mean_time_to_resolve_issues_twilio
          viz_type  = "timeseries"
          title     = "Mean time to resolve issues for Twilio Org (SLO <=180 days)"
        }
      }

      widget {
        alert_graph_definition {
          alert_id  = local.monitor_ids.mean_time_to_contact_issues_twilio
          viz_type  = "timeseries"
          title     = "Mean time to contact for Issues for Twilio Org (SLO <= 30 days)"
        }
      }

      widget {
        alert_graph_definition {
          alert_id  = local.monitor_ids.mean_time_to_contact_prs_twilio
          viz_type  = "timeseries"
          title     = "Mean time to contact for PRs for Twilio Org (SLO <= 10 days)"
        }
      }
    }
  }

  widget {
    group_definition {
      layout_type = "ordered"
      title       = "Leading SLI Metrics"
      show_title = true
      background_color = "vivid_yellow"

      widget {
        alert_graph_definition {
          alert_id  = local.monitor_ids.max_time_to_contact_issue_twilio
          viz_type  = "timeseries"
          title     = "Max time awaiting contact for issues for Twilio Org (SLO <= 10 days)"
        }
      }

      widget {
        alert_graph_definition {
          alert_id  = local.monitor_ids.max_time_to_contact_prs_twilio
          viz_type  = "timeseries"
          title     = "Max time awaiting contact for PRs for Twilio Org (SLO <= 7 days)"
        }
      }

      widget {
        alert_graph_definition {
          alert_id  = local.monitor_ids.max_time_to_resolve_issues_twilio
          viz_type  = "timeseries"
          title     = "Max time issues awaiting resolution for Twilio Org (SLO <= 90 days)"
        }
      }
    }
  }

  widget {
    group_definition {
      layout_type = "ordered"
      title       = "Twilio Helper Library Releases"
      show_title = true
      background_color = "vivid_purple"

      widget {
        timeseries_definition {
          title = "Release Count"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:library.release.count{*} by {repo,pre-release}"
                name        = "query1"
              }
            }
            display_type = "bars"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
        }
      }

      widget {
        timeseries_definition {
          title = "Release Status"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:library.release.status{*} by {repo,pre-release}.fill(last, 10000)"
                name        = "query1"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
        }
      }

      widget {
        event_stream_definition {
          query       = "source:github"
          event_size  = "s"
          title       = "Events for Twilio Github Repos"
        }
      }
    }
  }

  widget {
    group_definition {
      layout_type = "ordered"
      title       = "CLI Metrics"
      show_title = true
      background_color = "vivid_green"

      widget {
        timeseries_definition {
          title = "Platform Executables cumulative download metrics"
          live_span = "1w"
          request {
            formula {
              alias = "rmp"
              formula_expression = "query1"
            }
            formula {
              alias = "deb"
              formula_expression = "query2"
            }
            formula {
              alias = "exe"
              formula_expression = "query3"
            }
            formula {
              alias = "pkg"
              formula_expression = "query4"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:twilio_cli.github_rpm_downloads.count{*}.as_count()"
                name        = "query1"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:twilio_cli.github_deb_downloads.count{*}.as_count()"
                name        = "query2"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:twilio_cli.github_exe_downloads.count{*}.as_count()"
                name        = "query3"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:twilio_cli.github_pkg_downloads.count{*}.as_count()"
                name        = "query4"
              }
            }
            display_type = "bars"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
        }
      }

      widget {
        timeseries_definition {
          title = "S3 Bucket Download Count"
          live_span = "1mo"
          request {
            formula {
              alias = "download count"
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:aws.s3.get_requests{bucketname:twilio-cli-prod}.as_count()"
                name        = "query1"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
        }
      }

      widget {
        query_value_definition {
          title = "S3 Downloads Count"
          live_span = "1y"
          autoscale = true
          precision = 2
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:aws.s3.get_requests{bucketname:twilio-cli-prod}.as_count()"
                name        = "query1"
                aggregator = "sum"
              }
            }
          }
        }
      }

      widget {
        timeseries_definition {
          title = "NPM downloads count"
          live_span = "1w"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:twilio_cli.npm_download.count{*}.as_count()"
                name        = "query1"
              }
            }
            display_type = "bars"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
        }
      }

      widget {
        query_value_definition {
          title = "NPM Downloads Count"
          live_span = "1y"
          autoscale = true
          precision = 2
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:twilio_cli.npm_download.count{*}.as_count()"
                name        = "query1"
                aggregator = "sum"
              }
            }
          }
        }
      }
    }
  }

  widget {
    group_definition {
      layout_type = "ordered"
      title       = "API Explorer"
      show_title = true
      background_color = "vivid_yellow"

      widget {
        timeseries_definition {
          title = "GETs and POSTs"
          request {
            formula {
              alias = "GET"
              formula_expression = "query1"
            }
            formula {
              alias = "POST"
              formula_expression = "query2"
            }
            formula {
              alias = "Total"
              formula_expression = "query1 + query2"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:ops.api_explorer_v2.loads{env:prod}.as_count()"
                name        = "query1"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:ops.api_explorer_v2.request{env:prod}.as_count()"
                name        = "query2"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
        }
      }

      widget {
        timeseries_definition {
          title = "GETs by mount/action/referrer"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:ops.api_explorer_v2.loads{env:prod} by {mount,action,referrer}.as_count()"
                name        = "query1"
              }
            }
            display_type = "bars"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
        }
      }

      widget {
        timeseries_definition {
          title = "POSTs by method/referrer"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:ops.api_explorer_v2.request{env:prod} by {method,referrer}.as_count()"
                name        = "query1"
              }
            }
            display_type = "bars"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
        }
      }

      widget {
        timeseries_definition {
          title = "404s by mount/action/referrer"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:ops.api_explorer_v2.unknown_referrer{env:prod} by {mount,action,referrer}.as_count()"
                name        = "query1"
              }
            }
            display_type = "bars"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
        }
      }
    }
  }

  widget {
    group_definition {
      layout_type = "ordered"
      title       = "Librarian Metrics"
      show_title = true
      background_color = "vivid_orange"

      widget {
        timeseries_definition {
          title = "Server - Normalized load"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "max:system.load.norm.1{env:dev,role:librarian,*} by {host}"
                name        = "query1"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
          yaxis {
            include_zero = true
            min = "auto"
            max = "auto"
            scale = "linear"
            label = ""
          }
          marker {
            display_type = "info dashed"
            label        = "investigate"
            value        = "0.75 < y < 1"
          }
          marker {
            display_type = "warning dashed"
            label        = "heavy load"
            value        = "1 < y < 5"
          }
          marker {
            display_type = "error dashed"
            label        = "critical"
            value        = "y > 5"
          }
        }
      }

      widget {
        timeseries_definition {
          title = "CPU Utilization by Host  (%)"
          request {
            formula {
              formula_expression = "query1"
            }
            formula {
              formula_expression = "query2"
            }
            formula {
              formula_expression = "query1 + query2"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.cpu.user{role:librarian,*}"
                name        = "query1"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.cpu.usage{role:librarian,*}"
                name        = "query2"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
          yaxis {
            include_zero = true
            min = "auto"
            max = "auto"
            scale = "linear"
            label = ""
          }
          marker {
            display_type = "error dashed"
            value        = "y = 60"
          }
        }
      }

      widget {
        timeseries_definition {
          title = "CPU usage (%)"
          request {
            formula {
              formula_expression = "query1"
            }
            formula {
              formula_expression = "query2"
            }
            formula {
              formula_expression = "query3"
            }
            formula {
              formula_expression = "query4"
            }
            formula {
              formula_expression = "query5"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.cpu.idle{role:librarian,*}"
                name        = "query1"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.cpu.system{role:librarian,*}"
                name        = "query2"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.cpu.iowait{role:librarian,*}"
                name        = "query3"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.cpu.user{role:librarian,*}"
                name        = "query4"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.cpu.stolen{role:librarian,*}"
                name        = "query5"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
          yaxis {
            include_zero = true
            min = "auto"
            max = "auto"
            scale = "linear"
            label = ""
          }
        }
      }

      widget {
        timeseries_definition {
          title = "Memory breakdown"
          request {
            formula {
              formula_expression = "query1"
            }
            formula {
              formula_expression = "query2 - query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:system.mem.usable{role:librarian,env:dev,*}"
                name        = "query1"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:system.mem.total{role:librarian,env:dev,*}"
                name        = "query2"
              }
            }
            display_type = "line"
            style {
              palette    = "cool"
              line_type  = "dashed"
              line_width = "normal"
            }
          }
          request {
            formula {
              formula_expression = "query0"
            }
            formula {
              formula_expression = "query1"
            }
            formula {
              formula_expression = "query1 - query0"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.mem.usable{role:librarian,env:prod,*}"
                name        = "query0"
              }
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.mem.total{role:librarian,env:prod,*}"
                name        = "query1"
              }
            }
            display_type = "line"
            style {
              palette    = "warm"
              line_type  = "solid"
              line_width = "normal"
            }
          }
          yaxis {
            include_zero = true
            min = "auto"
            max = "auto"
            scale = "linear"
            label = ""
          }
        }
      }

      widget {
        hostmap_definition {
          request {
            fill {
              q = "avg:system.cpu.idle{role:librarian,*} by {host}"
            }
          }
          group           = ["realm", "availability-zone"]
          no_group_hosts  = true
          no_metric_hosts = true
          scope           = ["role:librarian"]
          style {
            palette      = "green_to_orange"
            palette_flip = true
          }
          title = "Hosts / Idle CPU"
        }
      }

      widget {
        timeseries_definition {
          title = "CPU IOWait by Host"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "avg:system.cpu.iowait{env:dev,*,role:librarian,*,*,*,*,*} by {host}"
                name        = "query1"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
            on_right_yaxis = false
          }
          yaxis {
            include_zero = true
            min = "auto"
            max = "auto"
            scale = "linear"
            label = ""
          }
        }
      }

      widget {
        timeseries_definition {
          title = "Disk usage by device (%)"
          request {
            formula {
              formula_expression = "query1 * 100"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "max:system.disk.in_use{role:librarian,*} by {device}"
                name        = "query1"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
          yaxis {
            include_zero = true
            min = "auto"
            max = "auto"
            scale = "linear"
            label = ""
          }
          marker {
            display_type = "error dashed"
            label        = "full"
            value        = "y = 100"
          }
        }
      }

      widget {
        timeseries_definition {
          title = "Disk latency (by device)"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "max:system.io.await{role:librarian,*} by {device}"
                name        = "query1"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
          yaxis {
            include_zero = true
            min = "auto"
            max = "auto"
            scale = "linear"
            label = ""
          }
        }
      }

      widget {
        timeseries_definition {
          title = "Docker - Running Containers"
          request {
            formula {
              formula_expression = "query1"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "sum:docker.containers.running{role:librarian,*} by {docker_image}"
                name        = "query1"
              }
            }
            display_type = "bars"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
          yaxis {
            include_zero = true
            min = "auto"
            max = "auto"
            scale = "linear"
            label = ""
          }
        }
      }

      widget {
        timeseries_definition {
          title = "Server - Free Memory (Mb)"
          request {
            formula {
              formula_expression = "query1 / 1000000"
            }
            query {
              metric_query {
                data_source = "metrics"
                query       = "min:system.mem.free{env:dev,role:librarian,*} by {host}"
                name        = "query1"
              }
            }
            display_type = "line"
            style {
              palette    = "classic"
              line_type  = "solid"
              line_width = "normal"
            }
          }
          yaxis {
            include_zero = true
            min = "auto"
            max = "auto"
            scale = "linear"
            label = ""
          }
        }
      }
    }
  }
}