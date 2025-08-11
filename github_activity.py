import json
import sys
import urllib.request
import urllib.error
import ssl

class github_activity():
    try:
        username=sys.argv[1]
    except IndexError:
        print("Error")
        sys.exit(1)

    api_url=f"https://api.github.com/users/{username}/events"
   
    context = ssl._create_unverified_context()
    try:
       with urllib.request.urlopen(api_url, context=context) as response:
            data = response.read()
            events = json.loads(data)

    except urllib.error.HTTPError as e:
        print(f"User name not found '{username}' Or Connection Error : {e.code}")
        sys.exit(1)
    if not events:
         print("No activites found for this user")
    else:
        print(f"Latest activity user  {username}:\n")
        for event in events:
            event_type = event.get('type')
            repo_name = event.get('repo', {}).get('name')
            if event_type == "PushEvent":
                commits = event.get('payload', {}).get('commits', [])
                if commits:
                    commits_count = len(commits)
                    print(f"- Pushed {commits_count} commit(s) to {repo_name}")
            elif event_type == "CreateEvent":
                ref_type = event.get('payload', {}).get('ref_type')
                if ref_type:
                    print(f"- Created a new {ref_type} in {repo_name}")
            elif event_type == "ForkEvent":
                print(f"- Forked {repo_name}")
            elif event_type == "PullRequestEvent":
                action = event.get('payload', {}).get('action')
                if action:
                    print(f"- {action.capitalize()} a pull request in {repo_name}")

