#дз2
import os
import subprocess
import yaml
import datetime
import graphviz

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_commits(repo_path, after_date):
    os.chdir(repo_path)
    result = subprocess.run(
        ['git', 'log', '--pretty=format:%H %cd', '--date=iso'],
        capture_output=True,
        text=True
    )
    
    commits = []
    for line in result.stdout.splitlines():
        hash_value, date = line.split(' ', 1)
        commit_date = datetime.datetime.fromisoformat(date)
        if commit_date > after_date:
            commits.append(hash_value)
    return commits

def build_graph(commits):
    dot = graphviz.Digraph(comment='Git Commit Dependencies')
    
    for commit in commits:
        dot.node(commit)
        # Здесь можно добавить логику для добавления зависимостей между коммитами
        # Например, если есть информация о родительских коммитах
        # parents = get_parents(commit)
        # for parent in parents:
        #     dot.edge(parent, commit)
    
    return dot

def save_graph(dot, output_path):
    dot.render(output_path, format='png', cleanup=True)

def main():
    config = load_config('config.yaml')
    after_date = datetime.datetime.fromisoformat(config['commit_date'])
    
    commits = get_commits(config['repository_path'], after_date)
    
    if not commits:
        print("No commits found after the specified date.")
        return
    
    graph = build_graph(commits)
    save_graph(graph, config['output_image_path'])
    
    print(f"Graph saved successfully to {config['output_image_path']}.")

if __name__ == "__main__":
    main()
