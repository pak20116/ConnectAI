<content>import unittest
import json
from unittest.mock import patch, MagicMock
from thumbnail_generator import generate_thumbnail

# Designer가 확정한 디자인 규칙을 가정 (실제로는 외부에서 로드되어야 함)
DESIGN_RULES = {
    "primary_color": "#2C3E50",
    "structure": "Focus->Escape",
    "contrast_ratio": 1.7,
    "style": "High Contrast, Minimalist"
}

class TestThumbnailGenerator(unittest.TestCase):

    @patch('thumbnail_generator.generate_thumbnail')
    def test_successful_generation(self, mock_generate):
        """테스트: 정상적인 스크립트와 규칙으로 썸네일 생성이 성공하는지 확인."""
        # Mocking the API call to simulate success
        mock_generate.return_value = "https://test.com/success_thumb.png"

        sample_script = "I struggled with setting up my system, but I finally found the escape path."
        
        result_url = generate_thumbnail(sample_script, DESIGN_RULES)
        
        self.assertEqual(result_url, "https://test.com/success_thumb.png")
        mock_generate.assert_called_once()

    @patch('thumbnail_generator.generate_thumbnail')
    def test_api_failure(self, mock_generate):
        """테스트: API 호출이 실패했을 때 적절히 에러를 처리하는지 확인."""
        # Mocking the API call to simulate failure (e.g., network error or invalid parameters)
        mock_generate.side_effect = Exception("API Rate Limit Exceeded")

        sample_script = "This script should fail gracefully."
        
        # 실제 환경에서는 try-except 블록이 필요하지만, 현재 함수 구조상 예외가 발생하면 그대로 반환되도록 가정하고 테스트합니다. 
        # (실제 구현 시에는 이 부분을 try/except로 감싸야 함)
        with self.assertRaises(Exception) as cm:
            generate_thumbnail(sample_script, DESIGN_RULES)
        
        self.assertIn("API Rate Limit Exceeded", str(cm.exception))

if __name__ == '__main__':
    unittest.main()</content>