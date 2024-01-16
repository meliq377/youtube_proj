import unittest
import os
from django.test import Client
from django.urls import reverse

class VideoDownloadTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        # Replace with a valid YouTube video URL
        self.video_url = "https://www.youtube.com/watch?v=RkfMKfUhsKY"  # Example URL

    def test_video_download(self):
        response = self.client.post(reverse('download_video'), {'video_url': self.video_url})

        # Assert successful response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'video/mp4')  # Or the appropriate content type

        # Check for expected file contents (optional)
        with open('downloaded_video.mp4', 'rb') as f:
            # Perform checks on the file contents, such as verifying the file type or initial bytes
            pass

        # Check for file existence (optional)
        self.assertTrue(os.path.exists('downloaded_video.mp4'))

if __name__ == '__main__':
    unittest.main()
