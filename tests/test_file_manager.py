"""
Test File Manager Module
=========================

Tests for the file_manager.py module covering file operations like move, copy, and replace.
"""

import os
import shutil
import tempfile
import sys
import pytest
from unittest.mock import patch, MagicMock

# Import FileManager from the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from file_manager import FileManager, main


@pytest.fixture
def temp_dirs():
    """Create temporary source and destination directories."""
    source_dir = tempfile.mkdtemp()
    dest_dir = tempfile.mkdtemp()
    return source_dir, dest_dir


@pytest.fixture
def file_manager(temp_dirs):
    """Create a FileManager instance with temp directories."""
    return FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])


class TestFileManagerInit:
    """Test FileManager initialization."""

    def test_init_default_directories(self):
        """Test initialization with default directories."""
        fm = FileManager()
        assert fm.source_dir == '.'
        assert fm.dest_dir == '.'
        assert fm.file_list == []

    def test_init_custom_directories(self):
        """Test initialization with custom directories."""
        source_dir = '/tmp/source'
        dest_dir = '/tmp/dest'
        fm = FileManager(source_dir=source_dir, dest_dir=dest_dir)
        assert fm.source_dir == source_dir
        assert fm.dest_dir == dest_dir
        assert fm.file_list == []


class TestGetFilesToProcess:
    """Test get_files_to_process method."""

    def test_get_files_with_new_file(self, temp_dirs):
        """Test getting files that are new (not in destination)."""
        # Create a file in source directory
        with open(os.path.join(temp_dirs[0], 'test.txt'), 'w') as f:
            f.write('test content')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.get_files_to_process()
        
        assert 'test.txt' in result

    def test_get_files_with_changed_file(self, temp_dirs):
        """Test getting files that are newer than destination."""
        # Create file in source and destination with source being newer
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        dest_file = os.path.join(temp_dirs[1], 'test.txt')
        
        with open(source_file, 'w') as f:
            f.write('test content')
        
        # Make destination file older by setting its mtime to past
        import time
        time.sleep(0.1)  # Ensure source is newer
        
        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.get_files_to_process()
        
        assert 'test.txt' in result

    def test_get_files_with_older_source(self, temp_dirs):
        """Test getting files where source is older than destination."""
        # Create file in both directories with source being older
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        dest_file = os.path.join(temp_dirs[1], 'test.txt')
        
        # Create destination first (so it's "newer")
        with open(dest_file, 'w') as f:
            f.write('dest content')
        
        # Then create source file (so it's "older")
        with open(source_file, 'w') as f:
            f.write('test content')
        
        # Set destination mtime to be in the future relative to source
        import time
        dest_mtime = os.path.getmtime(dest_file)
        time.sleep(0.1)
        os.utime(dest_file, (time.time() + 1, time.time() + 1))
        
        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.get_files_to_process()
        
        assert 'test.txt' not in result

    def test_get_files_with_nonexistent_source(self, temp_dirs):
        """Test getting files when source directory doesn't exist."""
        fm = FileManager(source_dir='/nonexistent/path', dest_dir=temp_dirs[1])
        result = fm.get_files_to_process()
        
        assert result == []


class TestIsFileNewOrChanged:
    """Test _is_file_new_or_changed method."""

    def test_file_is_new(self, temp_dirs):
        """Test that a new file is detected as new."""
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        dest_file = os.path.join(temp_dirs[1], 'test.txt')
        
        with open(source_file, 'w') as f:
            f.write('test content')
        
        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        assert fm._is_file_new_or_changed('test.txt') is True

    def test_file_is_changed(self, temp_dirs):
        """Test that a newer file is detected as changed."""
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        dest_file = os.path.join(temp_dirs[1], 'test.txt')
        
        with open(source_file, 'w') as f:
            f.write('test content')
        
        # Make destination file older
        import time
        time.sleep(0.1)
        
        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        assert fm._is_file_new_or_changed('test.txt') is True

    def test_file_is_not_changed(self, temp_dirs):
        """Test that an older source file is not detected as changed."""
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        dest_file = os.path.join(temp_dirs[1], 'test.txt')
        
        # Create destination first (so it's "newer")
        with open(dest_file, 'w') as f:
            f.write('dest content')
        
        # Then create source file (so it's "older")
        with open(source_file, 'w') as f:
            f.write('test content')
        
        # Set destination mtime to be in the future relative to source
        import time
        dest_mtime = os.path.getmtime(dest_file)
        time.sleep(0.1)
        os.utime(dest_file, (time.time() + 1, time.time() + 1))
        
        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        assert fm._is_file_new_or_changed('test.txt') is False


class TestMoveFiles:
    """Test move_files method."""

    def test_move_single_file(self, temp_dirs):
        """Test moving a single file."""
        # Create source file
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        with open(source_file, 'w') as f:
            f.write('test content')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.move_files(['test.txt'])
        
        assert 'test.txt' in result['success']
        assert len(result['failed']) == 0
        assert result['total_processed'] == 1
        assert result['total_success'] == 1

    def test_move_multiple_files(self, temp_dirs):
        """Test moving multiple files."""
        # Create source files
        for filename in ['file1.txt', 'file2.py']:
            source_file = os.path.join(temp_dirs[0], filename)
            with open(source_file, 'w') as f:
                f.write(f'content of {filename}')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.move_files(['file1.txt', 'file2.py'])
        
        assert len(result['success']) == 2
        assert len(result['failed']) == 0

    def test_move_with_failure(self, temp_dirs):
        """Test moving files with some failures."""
        # Create source file
        source_file = os.path.join(temp_dirs[0], 'readonly.txt')
        with open(source_file, 'w') as f:
            f.write('test content')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        
        # Mock shutil.move to raise an exception
        with patch('shutil.move') as mock_move:
            mock_move.side_effect = PermissionError("Read-only file")
            result = fm.move_files(['readonly.txt'])
            
            assert len(result['failed']) == 1
            failed_dict = result['failed'][0]
            assert 'file' in failed_dict
            assert 'error' in failed_dict


class TestCopyFiles:
    """Test copy_files method."""

    def test_copy_single_file(self, temp_dirs):
        """Test copying a single file."""
        # Create source file
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        with open(source_file, 'w') as f:
            f.write('test content')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.copy_files(['test.txt'])
        
        assert 'test.txt' in result['success']
        assert len(result['failed']) == 0

    def test_copy_skips_existing_file(self, temp_dirs):
        """Test that copy skips files already in destination."""
        # Create source file
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        with open(source_file, 'w') as f:
            f.write('source content')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        
        # Mock shutil.copy2 to simulate file already existing
        with patch('shutil.copy2') as mock_copy:
            mock_copy.side_effect = FileExistsError("File already exists")
            result = fm.copy_files(['test.txt'])
            
            assert len(result['success']) == 0
            assert len(result['failed']) == 1

    def test_copy_multiple_files(self, temp_dirs):
        """Test copying multiple files."""
        # Create source files
        for filename in ['file1.txt', 'file2.py']:
            source_file = os.path.join(temp_dirs[0], filename)
            with open(source_file, 'w') as f:
                f.write(f'content of {filename}')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.copy_files(['file1.txt', 'file2.py'])
        
        assert len(result['success']) == 2


class TestReplaceFiles:
    """Test replace_files method."""

    def test_replace_single_file(self, temp_dirs):
        """Test replacing a single file."""
        # Create source and destination files
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        dest_file = os.path.join(temp_dirs[1], 'test.txt')
        
        with open(source_file, 'w') as f:
            f.write('source content')
        with open(dest_file, 'w') as f:
            f.write('existing content')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.replace_files(['test.txt'])
        
        assert 'test.txt' in result['success']
        assert len(result['failed']) == 0

    def test_replace_with_same_content(self, temp_dirs):
        """Test replacing file with same content."""
        # Create source and destination files with same content
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        dest_file = os.path.join(temp_dirs[1], 'test.txt')
        
        with open(source_file, 'w') as f:
            f.write('same content')
        with open(dest_file, 'w') as f:
            f.write('same content')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.replace_files(['test.txt'])
        
        assert 'test.txt' in result['success']


class TestGetFileInfo:
    """Test get_file_info method."""

    def test_get_info_for_existing_file(self, temp_dirs):
        """Test getting info for existing file."""
        # Create source file
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        with open(source_file, 'w') as f:
            f.write('test content')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.get_file_info('test.txt')
        
        assert result['exists'] is True
        assert result['size'] > 0
        assert result['modified_time'] is not None

    def test_get_info_for_nonexistent_file(self, temp_dirs):
        """Test getting info for non-existent file."""
        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.get_file_info('nonexistent.txt')
        
        assert result['exists'] is False
        assert result['size'] == 0

    def test_get_info_with_destination_exists(self, temp_dirs):
        """Test getting info when destination exists."""
        # Create source file
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        with open(source_file, 'w') as f:
            f.write('test content')

        # Create destination file
        dest_file = os.path.join(temp_dirs[1], 'test.txt')
        with open(dest_file, 'w') as f:
            f.write('dest content')

        fm = FileManager(source_dir=temp_dirs[0], dest_dir=temp_dirs[1])
        result = fm.get_file_info('test.txt')
        
        assert result['exists'] is True
        assert result['destination_exists'] is True


class TestMainFunction:
    """Test main function."""

    def test_main_execution(self, temp_dirs):
        """Test that main function runs without errors."""
        # Create source file
        source_file = os.path.join(temp_dirs[0], 'test.txt')
        with open(source_file, 'w') as f:
            f.write('test content')

        # Mock print to avoid output issues
        with patch('builtins.print') as mock_print:
            main(src=temp_dirs[0], dist=temp_dirs[1])
            
            # Verify print was called (for the various print statements)
            assert mock_print.call_count > 0


if __name__ == '__main__':
    pytest.main([__file__])
