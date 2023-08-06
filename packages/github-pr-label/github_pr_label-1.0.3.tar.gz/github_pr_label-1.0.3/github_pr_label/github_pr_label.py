# Version   Date        Author      Description
# 1.0       07/10/2021  Paul        Linter
import sys
import os
import json
from github import Github

class PRLabel():
    """PRLabel class
    """
    def __init__(self, pr_url="",token='',github_api = 'https://api.github.com',label_json='./github_pr_label/labels.json'):
        self.token = token if token == '' else os.getenv("github_token")
        if self.token is None:
            print('Error','Not github connection token set in environment, exit')
            exit(1)
        self.label_json = label_json
        self.g = Github(base_url=github_api, login_or_token=self.token, verify=False)
        url_ll = pr_url.split("/")
        if len(url_ll) == 7: 
            self.repo_name, self.pr_number = url_ll[-4] + \
                "/" + url_ll[-3], int(url_ll[-1])
            print(f"inital label bot repo: {self.repo_name} PR:{self.pr_number}")
            self.repo = self.g.get_repo(self.repo_name)
            self.pr = self.repo.get_pull(self.pr_number)
        else:
            self.repo = None
            self.pr = None
            print('Error',f'PR is not in right format:{pr_url}')
            exit (1)
        self.labels = self.get_label_list()
        self.set_label("project",label_name)
          
    def set_pr_size_label(self):
        changes = self.pr.raw_data['additions'] + self.pr.raw_data['deletions'] + self.pr.raw_data['changed_files']
        _size = 'XS'
        if changes > 1000:
            _size = 'XXL'
        elif changes > 500:
            _size = 'XL'
        elif changes > 100:
            _size = 'L'
        elif changes > 30:
            _size = 'M'
        elif changes > 10:
            _size = 'S' 
        else:
            _size = 'XS' 
        self.set_label("size", _size)
                                                   
    def set_label(self, label_group, label_name):
        try:
            n,c,d = self.labels[label_group][label_name].split("|")
        except Exception as e:
            print(f'{label_group},{label_name} not found \n{e}')
            return
                    
        if self.labels[label_group]["replace"]:
            for lb in self.pr.get_labels() :
                print(f'current label: {lb.name}  {lb.color}  {lb.description}')
                # finds = set(self.pr_labels).intersection(self.labels[label_group])
                # for lb in finds:
                if lb.name.startswith(label_group):
                    if lb.name != n:
                        print(f'remove label: {lb.name}, replace with {n}')
                        self.pr.remove_from_labels(lb.name)
                    else : 
                        print(f'same label: {lb.name} == {n}')        
                        return
        self.label_exists(n,c,d)
        self.pr.add_to_labels(n)
        print(f'added label: {n} {c} {d}')
        
    def add_pr_reviewers(self, pr_reviewers):
        self.pr.create_review_request(pr_reviewers)

    def get_reviewers(self):
        return self.pr.get_reviews()

    def label_exists(self,n,c,d):
        for lb in self.repo.get_labels():
            if lb.name == n :
                if lb.color == c and lb.description == d:
                    print(f'found label {n}')
                    return 
                else:
                    print(f'need modify label:{lb.color}!={c} {lb.description} !={d}')
        
        print(f'create label name: {n}, color: {c}, desc: {d}')
        try:
            self.repo.create_label(n,c,d)
        except Exception as e :
            print(f'Error to create label name: {n}, color: {c}, desc: {d}\n {e}')

    def create_issue_comment(self, cm):
        self.pr.create_issue_comment(cm)
        
    def get_label_list(self):
        with open (self.label_json,'r') as f:
            return json.load(f)

## assigned, closed
if __name__ == "__main__":
    pr_url, label_group, label_name = sys.argv[1],sys.argv[2],sys.argv[3]
    bot = PRLabel(pr_url)
    bot.set_pr_size_label()
    if label_name != 'unknown':
        bot.set_label(label_group,label_name)
