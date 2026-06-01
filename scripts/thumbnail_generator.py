import json
from PIL import Image, ImageDraw, ImageFont
import os

# --- 1. Design & Configuration ---
class ThumbnailConfig:
    """Designer가 정의한 디자인 원칙을 클래스로 캡슐화합니다."""
    PRIMARY_COLOR = "#2C3E50"  # Dark Slate Gray (Focus)
    ACCENT_COLOR = "#E74C3C"   # Vivid Red/Orange (Escape)
    FONT_PATH = "Montserrat-Bold.ttf" # 실제 시스템에 설치된 폰트 경로로 수정 필요

class FocusEscapeTemplate:
    """Focus -> Escape 흐름을 시각화하는 레이아웃 구조."""
    ZONE_A_FOCUS = {"area": "top_heavy", "color": ThumbnailConfig.PRIMARY_COLOR, "text_role": "Pain"}
    ZONE_B_TRANSITION = {"area": "center_path", "color": ThumbnailConfig.PRIMARY_COLOR, "effect": "arrow"}
    ZONE_C_ESCAPE = {"area": "bottom_light", "color": ThumbnailConfig.ACCENT_COLOR, "text_role": "Freedom"}

class ThumbnailGenerator:
    """썸네일 생성을 위한 핵심 엔진."""
    def __init__(self, config: ThumbnailConfig, template: FocusEscapeTemplate):
        self.config = config
        self.template = template
        print("ThumbnailGenerator 초기화 완료: Focus -> Escape 템플릿 로드.")

    def process_data(self, video_data: dict) -> dict:
        """입력 데이터를 기반으로 레이아웃 및 텍스트를 준비합니다."""
        print("\n[InputHandler] 데이터 분석 시작...")
        # 실제로는 여기서 video_data를 분석하여 ZONE A, B, C에 들어갈 텍스트와 이미지 URL을 결정해야 함.
        
        results = {}
        results['zones'] = []

        # Zone A: Focus (Pain) 처리 로직 정의
        zone_a = self.template.ZONE_A_FOCUS
        results['zones'].append(zone_a)

        # Zone B: Transition (System) 처리 로직 정의
        zone_b = self.template.ZONE_B_TRANSITION
        results['zones'].append(zone_b)

        # Zone C: Escape (Freedom) 처리 로직 정의
        zone_c = self.template.ZONE_C_ESCAPE
        results['zones'].append(zone_c)
        
        print("[DesignEngine] 레이아웃 구조 확정 완료.")
        return results

    def generate_image(self, layout_data: dict, output_path: str):
        """실제 이미지 파일을 생성하고 저장하는 함수 (Placeholder)."""
        print(f"\n[ImageGenerator] {output_path} 경로에 최종 이미지를 생성합니다...")
        
        try:
            img = Image.new('RGB', (1280, 720), color='white') # 기본 크기 설정
            draw = ImageDraw.Draw(img)

            # Zone A 그리기 (Focus - Dark)
            zone_a = layout_data['zones'][0]
            draw.rectangle([0, 0, 1280, 350], fill=zone_a['color'])
            draw.text((50, 50), "FOCUS: [Pain Statement Placeholder]", fill="white", font=ImageFont.truetype(self.config.FONT_PATH, 40))

            # Zone B 그리기 (Transition - Path)
            zone_b = layout_data['zones'][1]
            draw.line([(640, 350), (640, 650)], fill=zone_b['color'], width=10) # 중앙 경로 강조
            draw.text((650, 450), "SYSTEM: [Solution Path Placeholder]", fill="white", font=ImageFont.truetype(self.config.FONT_PATH, 30))

            # Zone C 그리기 (Escape - Bright)
            zone_c = layout_data['zones'][2]
            draw.rectangle([0, 350, 1280, 720], fill=zone_c['color'])
            draw.text((640, 550), "ESCAPE: [Freedom Result Placeholder]", fill="white", font=ImageFont.truetype(self.config.FONT_PATH, 40))

            img.save(output_path)
            print(f"✅ 이미지 성공적으로 저장됨: {output_path}")

        except Exception as e:
            print(f"❌ 이미지 생성 중 오류 발생! (파일 시스템/폰트 확인 필요): {e}")


def main():
    """메인 실행 함수."""
    # 1. 환경 설정 로드
    config = ThumbnailConfig()
    template = FocusEscapeTemplate()

    # 2. 엔진 초기화
    generator = ThumbnailGenerator(config, template)

    # 3. 가상 입력 데이터 (실제로는 InputHandler에서 동적 로드됨)
    mock_video_data = {
        "hook_text": "당신이 모르는 실패 신호 3가지로 인생을 바꾼 방법",
        "focus_pain": "시간 낭비와 끝없는 불안감",
        "escape_result": "완전한 해방과 통제감"
    }

    # 4. 데이터 처리 및 레이아웃 준비
    layout_data = generator.process_data(mock_video_data)

    # 5. 이미지 생성 실행
    output_filename = "thumbnail_draft.png"
    generator.generate_image(layout_data, output_filename)


if __name__ == "__main__":
    main()