"""
File Manager Module
===================

A utility module for moving and overwriting files between directories.
This module provides functionality to copy, move, and replace files
without using Git operations - purely file system based operations.

Usage:
------
    from file_manager import FileManager
    
    # Create a manager instance
    fm = FileManager(source_dir='src', dest_dir='dist')
    
    # Move and overwrite existing files
    fm.move_files(['file1.py', 'file2.py'])
    
    # Copy files (without overwriting)
    fm.copy_files(['file1.py', 'file2.py'])
    
    # Get list of files to process
    file_list = fm.get_files_to_process()

Author: Engineering Team
Version: 1.0.0
"""

import os
import shutil


class FileManager:
    """
    FileManager class for managing file operations between directories.
    
    This class provides methods to move, copy, and replace files
    between source and destination directories without Git dependency.
    
    Attributes:
        source_dir (str): The source directory containing files to process.
        dest_dir (str): The destination directory where files will be placed.
        file_list (list): List of files to process.
    """
    
    def __init__(self, source_dir: str = '.', dest_dir: str = '.'):
        """
        Initialize FileManager with source and destination directories.
        
        Args:
            source_dir (str): Source directory path. Defaults to current directory.
            dest_dir (str): Destination directory path. Defaults to current directory.
        """
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.file_list = []
    
    def get_files_to_process(self) -> list:
        """
        Get list of files from source directory that are new or modified.
        
        This method identifies files in the source directory that need to be
        processed (moved/copied) to the destination directory. Files are identified
        based on their modification status relative to a baseline snapshot.
        
        Returns:
            list: List of file paths relative to source_dir.
        """
        self.file_list = []
        
        try:
            # Get all files from source directory
            source_files = [f for f in os.listdir(self.source_dir) 
                           if os.path.isfile(os.path.join(self.source_dir, f))]
            
            # Filter based on modification status (new or changed files)
            self.file_list = [f for f in source_files 
                             if self._is_file_new_or_changed(f)]

            print(f"Source files - {self.source_dir}: {source_files}")
            
        except FileNotFoundError:
            print(f"Source directory '{self.source_dir}' not found.")
            return []
        
        return self.file_list
    
    def _is_file_new_or_changed(self, filename: str) -> bool:
        """
        Determine if a file is new or has been changed.
        
        This method checks if a file's modification time indicates it's
        newer than the last known state (stored in metadata).
        
        Args:
            filename (str): Name of the file to check.
            
        Returns:
            bool: True if file is new or changed, False otherwise.
        """
        try:
            source_file_path = os.path.join(self.source_dir, filename)
            dest_file_path = os.path.join(self.dest_dir, filename)
            
            # Check if source file exists
            if not os.path.exists(source_file_path):
                return False
            
            # If destination doesn't exist or is older than source, it's new/changed
            if not os.path.exists(dest_file_path):
                return True
            
            source_mtime = os.path.getmtime(source_file_path)
            dest_mtime = os.path.getmtime(dest_file_path)
            
            return source_mtime > dest_mtime
            
        except OSError:
            # If we can't access files, assume it's new/changed
            return True
    
    def move_files(self, file_list: list = None) -> dict:
        """
        Move and overwrite existing files from source to destination.
        
        This method moves files from the source directory to the destination
        directory, overwriting any existing files in the destination.
        
        Args:
            file_list (list): List of file names to process. 
                             If None, uses self.file_list from get_files_to_process().
            
        Returns:
            dict: Dictionary containing operation results with keys:
                   - 'success': list of successfully moved files
                   - 'failed': list of failed operations with error messages
                   - 'total_processed': total number of files attempted
                   - 'total_success': count of successful operations
                   - 'total_failed': count of failed operations
        """
        if file_list is None:
            file_list = self.file_list
        
        results = {
            'success': [],
            'failed': [],
            'total_processed': len(file_list),
            'total_success': 0,
            'total_failed': 0
        }
        
        for filename in file_list:
            source_path = os.path.join(self.source_dir, filename)
            dest_path = os.path.join(self.dest_dir, filename)
            
            try:
                # Move the file (overwrites if exists)
                shutil.move(source_path, dest_path)
                
                results['success'].append(filename)
                results['total_success'] += 1
                
            except Exception as e:
                results['failed'].append({
                    'file': filename,
                    'error': str(e)
                })
                results['total_failed'] += 1
        
        return results
    
    def copy_files(self, file_list: list = None) -> dict:
        """
        Copy files from source to destination without overwriting.
        
        This method copies files from the source directory to the destination
        directory, only if the destination file does not already exist.
        
        Args:
            file_list (list): List of file names to process. 
                             If None, uses self.file_list from get_files_to_process().
            
        Returns:
            dict: Dictionary containing operation results with keys:
                   - 'success': list of successfully copied files
                   - 'failed': list of failed operations with error messages
                   - 'total_processed': total number of files attempted
                   - 'total_success': count of successful operations
                   - 'total_failed': count of failed operations
        """
        if file_list is None:
            file_list = self.file_list
        
        results = {
            'success': [],
            'failed': [],
            'total_processed': len(file_list),
            'total_success': 0,
            'total_failed': 0
        }
        
        for filename in file_list:
            source_path = os.path.join(self.source_dir, filename)
            dest_path = os.path.join(self.dest_dir, filename)
            
            try:
                # Only copy if destination doesn't exist
                if not os.path.exists(dest_path):
                    shutil.copy2(source_path, dest_path)
                    
                    results['success'].append(filename)
                    results['total_success'] += 1
                else:
                    print(f"Skipping '{filename}' - file already exists in destination")
                    
            except Exception as e:
                results['failed'].append({
                    'file': filename,
                    'error': str(e)
                })
                results['total_failed'] += 1
        
        return results
    
    def replace_files(self, file_list: list = None) -> dict:
        """
        Replace files in destination directory with source files.
        
        This method replaces existing files in the destination directory
        with corresponding files from the source directory.
        
        Args:
            file_list (list): List of file names to process. 
                             If None, uses self.file_list from get_files_to_process().
            
        Returns:
            dict: Dictionary containing operation results with keys:
                   - 'success': list of successfully replaced files
                   - 'failed': list of failed operations with error messages
                   - 'total_processed': total number of files attempted
                   - 'total_success': count of successful operations
                   - 'total_failed': count of failed operations
        """
        if file_list is None:
            file_list = self.file_list
        
        results = {
            'success': [],
            'failed': [],
            'total_processed': len(file_list),
            'total_success': 0,
            'total_failed': 0
        }
        
        for filename in file_list:
            source_path = os.path.join(self.source_dir, filename)
            dest_path = os.path.join(self.dest_dir, filename)
            
            try:
                # Remove existing destination file if present
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                
                # Copy the file (overwriting)
                shutil.copy2(source_path, dest_path)
                    
                results['success'].append(filename)
                results['total_success'] += 1
                
            except Exception as e:
                results['failed'].append({
                    'file': filename,
                    'error': str(e)
                })
                results['total_failed'] += 1
        
        return results
    
    def get_file_info(self, filename: str) -> dict:
        """
        Get information about a file in the source directory.
        
        Args:
            filename (str): Name of the file to get info for.
            
        Returns:
            dict: Dictionary containing file information including:
                   - 'exists': whether file exists in source
                   - 'size': file size in bytes
                   - 'modified_time': modification time as timestamp
                   - 'destination_exists': whether file exists in destination
        """
        source_path = os.path.join(self.source_dir, filename)
        dest_path = os.path.join(self.dest_dir, filename)
        
        result = {
            'exists': os.path.exists(source_path),
            'size': 0,
            'modified_time': None,
            'destination_exists': os.path.exists(dest_path)
        }
        
        if result['exists']:
            stat_info = os.stat(source_path)
            result['size'] = stat_info.st_size
            result['modified_time'] = stat_info.st_mtime
        
        return result


def main(src='workspace', dist='.'):
    """
    Main function demonstrating FileManager usage.
    
    This example shows how to use the FileManager class to move and
    replace files between directories.
    """
    # Create a manager instance with different source and destination directories
    fm = FileManager(source_dir=src, dest_dir=dist)
    
    # Get list of files to process (new or changed files)
    file_list = fm.get_files_to_process()
    
    print(f"Files to process: {file_list}")
    
    # Move files (overwriting existing ones in destination)
    move_result = fm.move_files(file_list)
    print(f"Move operation result: {move_result}")
    
    # Copy files (only if destination doesn't exist)
    copy_result = fm.copy_files(file_list)
    print(f"Copy operation result: {copy_result}")
    
    # Replace files (removing existing and overwriting)
    replace_result = fm.replace_files(file_list)
    print(f"Replace operation result: {replace_result}")


if __name__ == '__main__':
    main()
