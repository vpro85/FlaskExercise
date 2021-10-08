<P>Hi! This app written using Flask and can be used to get some information about github repos.</P>
<b>There are 5 endpoints:</b>
<li>/{<b>repo_owner</b>}/{<b>repo_name</b>} - this gives you information about current repo
<li>/{<b>repo_owner</b>}/{<b>repo_name</b>}/<b>pulls</b> - this gives you information about all pull request in current repo
<li>/{<b>repo_owner</b>}/{<b>repo_name</b>}/<b>oldpulls</b> - also gives you information about pull requests but this requests are older than 2 weeks
<li>/{<b>repo_owner</b>}/{<b>repo_name</b>}/<b>issues</b> - this gives you information about all issues in current repo
<li>/{<b>repo_owner</b>}/{<b>repo_name</b>}/<b>forks</b> - this gives you information about all forks of current repo

In each endpoint you should give 2 parameters: string {repo_owner} and string {repo_name}. 
