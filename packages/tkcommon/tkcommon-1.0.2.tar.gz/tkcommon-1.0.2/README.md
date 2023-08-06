# tkcommon

tkcommon is a collection of small Python functions and classes for building scripts and internal tools.

Installation
-----
The package can be installed through `pip`:
```bash
pip install tkcommon
```

Usage
-----

```python
from tkcommon import get_logger, post_to_slack
from tkcommon import init_config, get_config
from tkcommon import create_jira_issue, update_jira_issue

logger = get_logger(__name__)
logger.info("Test log")

post_to_slack(message="Test slack message")

init_config(from_env=True, json_file="./config.json")
secret = get_config(
    "mongo_connection", "mongodb://user:password@localhost:27017/database"
)

issue_fields = {
    "project": {"id": 123},
    "summary": "New issue from jira-python",
    "description": "Look into this one",
    "issuetype": {"name": "Bug"},
}
issue = create_jira_issue(issue_fields)

update_issue_fields = {
    "summary": "New issue from jira-python",
    "description": "Look into this one",
}
issue = update_jira_issue(jira_id="CDMS-1234", fields=update_issue_fields, notify=True)
```