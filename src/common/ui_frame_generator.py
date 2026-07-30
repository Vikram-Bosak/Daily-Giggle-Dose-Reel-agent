import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji

def generate_ui_frame(output_path: str, source_name: str, headline: str, story: str, width=1080, height=1920):
    # Create a solid white background (completely white)
    img = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Fonts (Platform-specific fallbacks)
    import platform
    if platform.system() == "Windows":
        font_bold = 'C:\\Windows\\Fonts\\arialbd.ttf'
        font_reg = 'C:\\Windows\\Fonts\\arial.ttf'
    else:
        font_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        font_reg = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

    # --- Draw Page Logo and Name at Top Left ---
    # Placed at x=75, y=120
    logo_path = os.path.join(os.path.dirname(__file__), "../../assets/custom_logo.png")
    if os.path.exists(logo_path):
        try:
            mask_logo = Image.new('L', (120, 120), 0)
            mask_logo_draw = ImageDraw.Draw(mask_logo)
            mask_logo_draw.ellipse((0, 0, 120, 120), fill=255)
            
            logo_img = Image.open(logo_path).convert("RGBA")
            logo_resized = logo_img.resize((120, 120), Image.LANCZOS)
            img.paste(logo_resized, (75, 120), mask_logo)
        except Exception as e:
            print(f"Error drawing circular logo: {e}")
            
    try:
        f_name = ImageFont.truetype(font_bold, 40)
        f_handle = ImageFont.truetype(font_reg, 32)
    except IOError:
        f_name = f_handle = ImageFont.load_default()

    # Draw Page Name
    draw.text((220, 125), "Daily Giggle Dose", fill=(0, 0, 0, 255), font=f_name)
    
    # Draw Verified Badge
    try:
        name_w = int(draw.textlength("Daily Giggle Dose", font=f_name))
    except AttributeError:
        bbox = draw.textbbox((0, 0), "Daily Giggle Dose", font=f_name)
        name_w = bbox[2] - bbox[0]
        
    badge_x = 220 + name_w + 12
    badge_y = 133
    draw.ellipse([badge_x, badge_y, badge_x + 28, badge_y + 28], fill=(0, 149, 246, 255))
    draw.line([badge_x + 9, badge_y + 14, badge_x + 13, badge_y + 18], fill=(255, 255, 255, 255), width=3)
    draw.line([badge_x + 13, badge_y + 18, badge_x + 20, badge_y + 9], fill=(255, 255, 255, 255), width=3)

    # Draw Handle
    draw.text((220, 180), "@dailygiggledose", fill=(100, 110, 120, 255), font=f_handle)
        
    def draw_all(renderer, is_pilmoji):
        # --- Wrapped Details/Description (Drawn inside the Top Area, just above the video) ---
        try:
            f_story = ImageFont.truetype(font_reg, 44)
        except IOError:
            f_story = ImageFont.load_default()
            
        text_to_draw = story.strip() if story else (headline.strip() if headline else "")
        # Limit text length to avoid drawing into the video area
        if len(text_to_draw) > 90:
            text_to_draw = text_to_draw[:87] + "..."
            
        # Wrap to max 42 characters per line
        wrapped_lines = textwrap.wrap(text_to_draw, width=42)
        wrapped_lines = wrapped_lines[:2]  # Limit to 2 lines
        
        y_offset = 300
        for line in wrapped_lines:
            if is_pilmoji:
                line_w = renderer.getsize(line, font=f_story)[0]
            else:
                try:
                    line_w = int(draw.textlength(line, font=f_story))
                except AttributeError:
                    bbox = draw.textbbox((0, 0), line, font=f_story)
                    line_w = bbox[2] - bbox[0]
            line_x = (width - line_w) // 2
            renderer.text((line_x, y_offset), line, fill=(0, 0, 0, 255), font=f_story)
            y_offset += 55

    try:
        with Pilmoji(img) as pilmoji:
            draw_all(pilmoji, is_pilmoji=True)
    except Exception as e:
        print(f"Pilmoji failed (network or other error): {e}. Falling back to standard ImageDraw.")
        draw_all(draw, is_pilmoji=False)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    return output_path

if __name__ == "__main__":
    pass
