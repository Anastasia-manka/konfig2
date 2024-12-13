#дз2
import os
import subprocess
import yaml
import datetime
import zoneinfo

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
    timezone = zoneinfo.ZoneInfo("Europe/Moscow")  # Укажите часовой пояс
    for line in result.stdout.splitlines():
        hash_value, date = line.split(' ', 1)
        commit_date = datetime.datetime.fromisoformat(date).replace(tzinfo=timezone)  # Исправлено
        if commit_date > after_date:
            commits.append(hash_value)
    return commits

def get_parents(commit):
    result = subprocess.run(
        ['git', 'rev-list', '--parents', '-n', '1', commit],
        capture_output=True,
        text=True
    )
    parents = result.stdout.strip().split()[1:]  # Первый элемент — сам коммит, остальные — родители
    return parents

def build_mermaid_graph(commits):
    mermaid_graph = "graph TD;\n"

    for commit in commits:
        mermaid_graph += f"    {commit};\n"  # Добавляем узел

        # Получаем родительские коммиты
        parents = get_parents(commit)
        for parent in parents:
            mermaid_graph += f"    {parent} --> {commit};\n"  # Добавляем ребро

    return mermaid_graph

def save_mermaid_graph(mermaid_graph, output_path):
    with open(output_path, 'w') as file:
        file.write(mermaid_graph)

def main():
    config = load_config('config.yaml')
    timezone = zoneinfo.ZoneInfo("Europe/Moscow")  # Укажите часовой пояс
    after_date = datetime.datetime.fromisoformat(config['commit_date']).replace(tzinfo=timezone)

    commits = get_commits(config['repository_path'], after_date)

    if not commits:
        print("No commits found after the specified date.")
        return

    mermaid_graph = build_mermaid_graph(commits)
    save_mermaid_graph(mermaid_graph, 'graph.mmd')  # Сохраняем описание графа

    print("Mermaid graph description saved to graph.mmd.")

    # Используем Mermaid CLI для генерации изображения
    subprocess.run(['mmdc', '-i', 'graph.mmd', '-o', config['output_image_path']])

    print(f"Graph saved successfully to {config['output_image_path']}.")

if __name__ == "__main__":
    main()
