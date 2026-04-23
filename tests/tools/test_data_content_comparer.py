"""
Tests for the Data Content Comparer tool.
"""

import pytest
import pandas as pd
from pathlib import Path
from typing import Tuple

# Import the tool for testing
try:
    from scriptcraft.tools.data_content_comparer.main import DataContentComparer
    from scriptcraft.tools.data_content_comparer.utils import compare_datasets, generate_report
except ImportError:
    pytest.skip("Data Content Comparer not available")


class TestDataContentComparer:
    """Test suite for DataContentComparer tool."""
    
    def test_tool_initialization(self):
        """Test that the tool initializes correctly."""
        comparer = DataContentComparer()
        assert comparer.name == "Data Content Comparer"
        assert "compares content between datasets" in comparer.description.lower()
    
    def test_basic_comparison(self, sample_comparison_files: Tuple[Path, Path], temp_output_dir: Path):
        """Test basic comparison functionality."""
        file1_path, file2_path = sample_comparison_files
        
        comparer = DataContentComparer()
        comparer.run(
            input_paths=[str(file1_path), str(file2_path)],
            output_dir=str(temp_output_dir)
        )
        
        # Check that output files were created
        output_files = list(temp_output_dir.glob("*.xlsx"))
        assert len(output_files) > 0, "No output files were created"
    
    def test_comparison_with_different_modes(self, sample_comparison_files: Tuple[Path, Path], temp_output_dir: Path):
        """Test comparison with different modes."""
        file1_path, file2_path = sample_comparison_files
        
        comparer = DataContentComparer()
        
        # Test standard mode
        comparer.run(
            input_paths=[str(file1_path), str(file2_path)],
            output_dir=str(temp_output_dir),
            mode="standard"
        )
        
        # Test full mode
        comparer.run(
            input_paths=[str(file1_path), str(file2_path)],
            output_dir=str(temp_output_dir),
            mode="full"
        )
    
    def test_error_handling_invalid_inputs(self, temp_output_dir: Path):
        """Test error handling with invalid inputs."""
        comparer = DataContentComparer()
        
        # Test with non-existent files
        with pytest.raises(ValueError, match="Need at least two input files"):
            comparer.run(
                input_paths=[],
                output_dir=str(temp_output_dir)
            )
        
        # Test with only one file
        with pytest.raises(ValueError, match="Need at least two input files"):
            comparer.run(
                input_paths=["nonexistent.csv"],
                output_dir=str(temp_output_dir)
            )
    
    def test_comparison_utils(self, sample_comparison_files: Tuple[Path, Path]):
        """Test the comparison utility functions."""
        file1_path, file2_path = sample_comparison_files
        
        # Load the data
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        
        # Test comparison function
        result = compare_datasets(df1, df2, comparison_type='full')
        assert isinstance(result, dict)
        assert 'detailed_analysis' in result
    
    def test_report_generation(self, sample_comparison_files: Tuple[Path, Path], temp_output_dir: Path):
        """Test report generation functionality."""
        file1_path, file2_path = sample_comparison_files
        
        # Load the data
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        
        # Create comparison result
        comparison_result = {
            'basic_comparison': {'shape': (4, 3)},
            'detailed_analysis': {'differences': 1}
        }
        
        # Test Excel report generation
        report_path = temp_output_dir / "test_report.xlsx"
        generate_report(comparison_result, report_path, format='excel')
        assert report_path.exists()
        
        # Test CSV report generation
        report_path_csv = temp_output_dir / "test_report.csv"
        generate_report(comparison_result, report_path_csv, format='csv')
        assert report_path_csv.exists()
    
    def test_large_dataset_handling(self, temp_output_dir: Path):
        """Test handling of larger datasets."""
        # Create larger test datasets
        large_data1 = {
            'ID': range(1000),
            'Name': [f'Person_{i}' for i in range(1000)],
            'Value': [i * 2 for i in range(1000)]
        }
        
        large_data2 = {
            'ID': range(1000),
            'Name': [f'Person_{i}' for i in range(1000)],
            'Value': [i * 2 + (1 if i % 10 == 0 else 0) for i in range(1000)]  # Some differences
        }
        
        df1 = pd.DataFrame(large_data1)
        df2 = pd.DataFrame(large_data2)
        
        file1_path = temp_output_dir / "large_file1.csv"
        file2_path = temp_output_dir / "large_file2.csv"
        
        df1.to_csv(file1_path, index=False)
        df2.to_csv(file2_path, index=False)
        
        comparer = DataContentComparer()
        comparer.run(
            input_paths=[str(file1_path), str(file2_path)],
            output_dir=str(temp_output_dir)
        )
        
        # Check that the comparison completed without errors
        output_files = list(temp_output_dir.glob("*.xlsx"))
        assert len(output_files) > 0


class TestDataContentComparerIntegration:
    """Integration tests for DataContentComparer."""
    
    def test_pipeline_integration(self, sample_comparison_files: Tuple[Path, Path], temp_output_dir: Path):
        """Test integration with the pipeline system."""
        file1_path, file2_path = sample_comparison_files
        
        # Test through the main runner
        from scriptcraft.common.cli import parse_tool_args
        
        # Simulate CLI arguments
        import sys
        original_argv = sys.argv
        try:
            sys.argv = [
                'test_data_content_comparer',
                '--input-paths', str(file1_path), str(file2_path),
                '--output-dir', str(temp_output_dir)
            ]
            
            args = parse_tool_args("Test Data Content Comparer")
            comparer = DataContentComparer()
            comparer.run(
                input_paths=args.input_paths,
                output_dir=args.output_dir
            )
            
            # Verify output
            output_files = list(temp_output_dir.glob("*.xlsx"))
            assert len(output_files) > 0
            
        finally:
            sys.argv = original_argv
    
    def test_workspace_integration(self, sample_comparison_files: Tuple[Path, Path], temp_output_dir: Path):
        """Test integration with the workspace workflow."""
        file1_path, file2_path = sample_comparison_files
        
        # Test that the tool works with the workspace configuration
        comparer = DataContentComparer()
        
        # This should work with the workspace's run_all.py system
        comparer.run(
            input_paths=[str(file1_path), str(file2_path)],
            output_dir=str(temp_output_dir),
            domain="test"  # Test domain parameter
        )
        
        # Verify the tool respects workspace conventions
        output_files = list(temp_output_dir.glob("*.xlsx"))
        assert len(output_files) > 0


class TestDataContentComparerPerformance:
    """Performance tests for DataContentComparer."""
    
    def test_memory_usage(self, temp_output_dir: Path):
        """Test memory usage with different dataset sizes."""
        import psutil
        import os
        
        # Create datasets of different sizes
        sizes = [100, 1000, 10000]
        
        for size in sizes:
            data1 = {
                'ID': range(size),
                'Name': [f'Person_{i}' for i in range(size)],
                'Value': [i * 2 for i in range(size)]
            }
            
            data2 = {
                'ID': range(size),
                'Name': [f'Person_{i}' for i in range(size)],
                'Value': [i * 2 + (1 if i % 10 == 0 else 0) for i in range(size)]
            }
            
            df1 = pd.DataFrame(data1)
            df2 = pd.DataFrame(data2)
            
            file1_path = temp_output_dir / f"perf_file1_{size}.csv"
            file2_path = temp_output_dir / f"perf_file2_{size}.csv"
            
            df1.to_csv(file1_path, index=False)
            df2.to_csv(file2_path, index=False)
            
            # Measure memory before
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            comparer = DataContentComparer()
            comparer.run(
                input_paths=[str(file1_path), str(file2_path)],
                output_dir=str(temp_output_dir)
            )
            
            # Measure memory after
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = memory_after - memory_before
            
            # Memory increase should be reasonable (less than 10x dataset size)
            expected_max_memory = size * 0.01  # 1% of dataset size in MB
            assert memory_increase < expected_max_memory, f"Memory usage too high for size {size}"
    
    def test_processing_speed(self, temp_output_dir: Path):
        """Test processing speed with different dataset sizes."""
        import time
        
        sizes = [100, 1000, 10000]
        
        for size in sizes:
            data1 = {
                'ID': range(size),
                'Name': [f'Person_{i}' for i in range(size)],
                'Value': [i * 2 for i in range(size)]
            }
            
            data2 = {
                'ID': range(size),
                'Name': [f'Person_{i}' for i in range(size)],
                'Value': [i * 2 + (1 if i % 10 == 0 else 0) for i in range(size)]
            }
            
            df1 = pd.DataFrame(data1)
            df2 = pd.DataFrame(data2)
            
            file1_path = temp_output_dir / f"speed_file1_{size}.csv"
            file2_path = temp_output_dir / f"speed_file2_{size}.csv"
            
            df1.to_csv(file1_path, index=False)
            df2.to_csv(file2_path, index=False)
            
            # Measure processing time
            start_time = time.time()
            
            comparer = DataContentComparer()
            comparer.run(
                input_paths=[str(file1_path), str(file2_path)],
                output_dir=str(temp_output_dir)
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Processing time should be reasonable (less than 1 second per 1000 rows)
            expected_max_time = size / 1000  # 1 second per 1000 rows
            assert processing_time < expected_max_time, f"Processing too slow for size {size}" 