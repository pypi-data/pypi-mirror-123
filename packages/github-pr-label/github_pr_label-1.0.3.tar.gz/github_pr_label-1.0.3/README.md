### Installation

```
pip install github-pr-label
```

### Example

```python
import github_pr_label
label_group = "bot"
label_name = "pass"
gh_label = github_pr_label.PRLabel(
    pr_url = "your_pr/number"
)
gh_label.set_label(label_group,label_name)

```


### label json file
for example
label: bot have three status [pass,fail,skip]
status: there are three parts to build a label and split by '|'
        name|colour|description

```json
{
    "bot": {
        "replace":true,
        "pass": "bot:heavy_check_mark:|3CBF00|passed bot test",
        "fail": "bot:x:|3CBF00|failed bot test",
        "skip": "bot:p:|E50009|bot no required"
    },
    "size":{
        "replace":true,
        "XS": "size/XS|3CBF00|<10 lines",
        "S": "size/S|5D9801|>10 lines",
        "M": "size/M|7F7203|>30 lines",
        "L": "size/L|A14C05|>100 lines",
        "XL": "size/XL|C32607|>500 lines",
        "XXL": "size/XXL|E50009|>1000 lines"
    }, 
}
```
### Size Auto Determination.

The Pull Request labels are applied depending on the total lines of code changed (additions + deletions).

| Name | Description |
| ---- | ----------- |
| <a id="size/XS" href="#size/XS">`size/XS`</a> | Denotes a PR that changes 0-9 lines. |
| <a id="size/S" href="#size/S">`size/S`</a> | Denotes a PR that changes 10-29 lines. |
| <a id="size/M" href="#size/M">`size/M`</a> | Denotes a PR that changes 30-99 lines. |
| <a id="size/L" href="#size/L">`size/L`</a> | Denotes a PR that changes 100-499 lines. |
| <a id="size/XL" href="#size/XL">`size/XL`</a> | Denotes a PR that changes 500-999 lines. |
| <a id="size/XXL" href="#size/XXL">`size/XXL`</a> | Denotes a PR that changes 1000+ lines. |


