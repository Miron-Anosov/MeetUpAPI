"""Watermark images util."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from src.core.settings.env import settings


def add_watermark(
    file_path: str,
    watermark_text: str = settings.wm.WATERMARK_TEXT,
) -> str:
    """Create image with watermark."""
    file_path_: Path = Path(file_path)

    with Image.open(file_path_) as original:
        original = original.convert("RGBA")
        watermark = Image.new("RGBA", original.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = original.width - text_width - 30
        y = original.height - text_height - 50

        draw.text(
            (x, y),
            watermark_text,
            fill=(255, 255, 255, settings.wm.OPACITY),
            font=font,
        )

        watermarked = Image.alpha_composite(original, watermark)
        output_path: Path = (
            file_path_.parent
            / f"{file_path_.stem}{settings.wm.POSTFIX}{file_path_.suffix}"
        )

        watermarked.convert("RGB").save(output_path, "JPEG", quality=95)

        return str(output_path)
