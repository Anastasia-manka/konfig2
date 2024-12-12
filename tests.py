import unittest
from unittest.mock import patch, mock_open, MagicMock
import datetime
import yaml
import graphviz
from dependency_visualizer import load_config, get_commits, build_graph, save_graph

class TestDependencyVisualizer(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='visualizer_path: ""\nrepository_path: "/path/to/repo"\noutput_image_path: "/path/to/output/image"\ncommit_date: "2023-01-01"\n')
    def test_load_config(self, mock_file):
        config = load_config('config.yaml')
        self.assertEqual(config['repository_path'], '/path/to/repo')
        self.assertEqual(config['output_image_path'], '/path/to/output/image')
        self.assertEqual(config['commit_date'], '2023-01-01')

    @patch('subprocess.run')
    @patch('os.chdir')
    def test_get_commits(self, mock_chdir, mock_run):
        mock_run.return_value.stdout = 'abc123 2023-01-02T12:00:00\nxyz789 2022-12-31T12:00:00'
        after_date = datetime.datetime(2023, 1, 1)
        
        commits = get_commits('/path/to/repo', after_date)
        self.assertIn('abc123', commits)
        self.assertNotIn('xyz789', commits)

    @patch('graphviz.Digraph')
    def test_build_graph(self, mock_Digraph):
        mock_graph = MagicMock()
        mock_Digraph.return_value = mock_graph
        
        commits = ['abc123', 'xyz789']
        graph = build_graph(commits)
        
        self.assertEqual(mock_Digraph.call_count, 1)
        self.assertEqual(mock_graph.node.call_count, 2)  # Два коммита
        self.assertIn('abc123', [call[0][0] for call in mock_graph.node.call_args_list])
        self.assertIn('xyz789', [call[0][0] for call in mock_graph.node.call_args_list])

    @patch('graphviz.Digraph.render')
    def test_save_graph(self, mock_render):
        mock_graph = MagicMock()
        output_path = '/path/to/output/image'
        
        save_graph(mock_graph, output_path)
        
        mock_graph.render.assert_called_once_with(output_path, format='png', cleanup=True)

if __name__ == '__main__':
    unittest.main()