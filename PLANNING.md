# Klaxer - A webhook alert proxy

*Klaxon, Klax-off*

**Problem**

In this increasingly agile and devops-driven world, developers have had their
inboxes decimated by a deluge of monitoring notifications.  It's become even
worse in the age of Slack (and family) because, unlike with email, there is no
way to filter the integrations spamming your channels to ensure that important
stuff gets seen.

**Solution**

Klaxer sits between your services (e.g., JIRA, GitLab, cron scripts) and your
messaging clients (Slack, for now) and applies rule-based logic to filter and
direct the incoming webhooks to a narrower audience.

## Features

1. Should accept webhooks from popular sources
2. Should be able to apply rules to them.
    ```python
    if message.source == 'JIRA':
        if message.type in ('comment', 'new_user'):
            return # discard
        elif 'created new issue' in message.subject.lower():
            alert(get_project_channel(message.destination))
    ```
    Idelly, these are scriptable and don't require actual code be written.
3. Users should be able to interact with the notification to manage the alerts.
   Check out message menus:
   (https://medium.com/slack-developer-blog/build-an-interactive-slack-app-with-message-menus-1fb2c6298308).
   Alerts can be muted (in which case Klaxer will try to disambiguate between
   repeat alerts vs. new ones), or snoozed.
4. Alerts can be targeted. Instead of simply posting to a channel, they can
   also be directed to a specific set of users via @-mentions in the message
   body.
5. If contiguous messages are posted for the same alert, the old messages are
   automatically deleted, reducing clutter.

## Requirements

Python 3.6 only. Try to minimize deps on external daemons/processes.
