import unittest
from app import format_needed_files, check_token_expiration, zip_files

class TestFormatNeededFiles(unittest.TestCase):

	def test_format_needed_files(self):
		files = ['file1', 'file2', 'file3', 'file4']
		expected = 'file1 \nfile2 \nfile3 \nfile4'
		self.assertEqual(format_needed_files(files), expected)
	
	def test_format_needed_files_with_empty_list(self):
		files = []
		expected = ''
		self.assertEqual(format_needed_files(files), expected)
	def test_format_needed_files_with_one_file(self):
		files = ['file1']
		expected = 'file1'
		self.assertEqual(format_needed_files(files), expected)

class TestCheckTokenExpiration(unittest.TestCase):

	def test_check_token_expiration(self):
		token_response = {'expires_in': 3600}
		print("check",check_token_expiration(token_response))
		self.assertEqual(check_token_expiration(token_response), token_response)
	
	def test_check_token_expiration_with_expired_token(self):
		token_response = {'expires_in': 0}
		self.assertEqual(check_token_expiration(token_response), token_response)

class TestZipFiles(unittest.TestCase):
	
	def test_zip_files(self):
		expected = ['filebackup_March2023_1.zip']
		self.assertEqual(zip_files(), expected)
	
	def test_zip_files_with_empty_list(self):
		expected = []
		self.assertEqual(zip_files(), expected)
	
	def test_zip_files_with_one_file(self):
		expected = ['filebackup_March2023_1.zip']
		self.assertEqual(zip_files(), expected)

if __name__ == '__main__':
	unittest.main()