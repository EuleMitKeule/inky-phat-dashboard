"""Tests for the image_generator module."""

import pytest

from inky_phat_dashboard.const import ColorMode, ColorPalette
from inky_phat_dashboard.image_generator import ImageGenerator
from inky_phat_dashboard.models import (
    Config,
    DashboardElementData,
    DashboardViewData,
    DetailedViewData,
    DetailedViewTwoLinesData,
)


@pytest.mark.skip()
def test_generate_detailed_view_light_mode(config: Config):
    """Test the generate_detailed_view method."""

    image_generator = ImageGenerator(config)

    detailed_view_data = DetailedViewData(
        "media/clock/clock_large.png",
        "22:30",
    )
    image = image_generator.generate_detailed_view(detailed_view_data)

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_detailed_view_dark_mode(config: Config):
    """Test the generate_detailed_view method."""

    config.color_mode = ColorMode.DARK

    image_generator = ImageGenerator(config)

    detailed_view_data = DetailedViewData(
        "media/clock/clock_large.png",
        "22:30",
    )
    image = image_generator.generate_detailed_view(detailed_view_data)

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_detailed_view_light_mode_alert(config: Config):
    """Test the generate_detailed_view method."""

    image_generator = ImageGenerator(config)

    detailed_view_data = DetailedViewData(
        "media/clock/clock_large.png",
        "22:30",
        is_border_alert=True,
        is_icon_alert=True,
        is_text_alert=True,
    )
    image = image_generator.generate_detailed_view(detailed_view_data)

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_detailed_view_dark_mode_alert(config: Config):
    """Test the generate_detailed_view method."""

    config.color_mode = ColorMode.DARK

    image_generator = ImageGenerator(config)

    detailed_view_data = DetailedViewData(
        "media/clock/clock_large.png",
        "22:30",
        is_border_alert=True,
        is_icon_alert=True,
        is_text_alert=True,
    )
    image = image_generator.generate_detailed_view(detailed_view_data)

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_detailed_view_dark_mode_alert_yellow(config: Config):
    """Test the generate_detailed_view method."""

    config.color_mode = ColorMode.DARK
    config.color_palette = ColorPalette.YELLOW

    image_generator = ImageGenerator(config)

    detailed_view_data = DetailedViewData(
        "media/clock/clock_large.png",
        "22:30",
        is_border_alert=True,
        is_icon_alert=True,
        is_text_alert=True,
    )
    image = image_generator.generate_detailed_view(detailed_view_data)

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_detailed_view_two_lines_light_mode(config: Config):
    """Test the generate_detailed_view method."""

    image_generator = ImageGenerator(config)

    detailed_view_two_lines_data = DetailedViewTwoLinesData(
        "media/waste/waste_large.png",
        "Restabfall",
        "In 2 Tagen",
    )
    image = image_generator.generate_detailed_view_two_lines(
        detailed_view_two_lines_data
    )

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_detailed_view_two_lines_dark_mode(config: Config):
    """Test the generate_detailed_view method."""

    config.color_mode = ColorMode.DARK

    image_generator = ImageGenerator(config)

    detailed_view_two_lines_data = DetailedViewTwoLinesData(
        "media/waste/waste_large.png",
        "Restabfall",
        "In 2 Tagen",
    )
    image = image_generator.generate_detailed_view_two_lines(
        detailed_view_two_lines_data
    )

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_detailed_view_two_lines_light_mode_alert(config: Config):
    """Test the generate_detailed_view method."""

    image_generator = ImageGenerator(config)

    detailed_view_two_lines_data = DetailedViewTwoLinesData(
        "media/waste/waste_large.png",
        "Restabfall",
        "In 2 Tagen",
        is_border_alert=True,
        is_icon_alert=True,
        is_upper_text_alert=True,
        is_lower_text_alert=True,
    )
    image = image_generator.generate_detailed_view_two_lines(
        detailed_view_two_lines_data
    )

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_detailed_view_two_lines_dark_mode_alert(config: Config):
    """Test the generate_detailed_view method."""

    config.color_mode = ColorMode.DARK

    image_generator = ImageGenerator(config)

    detailed_view_two_lines_data = DetailedViewTwoLinesData(
        "media/waste/waste_large.png",
        "Restabfall",
        "In 2 Tagen",
        is_border_alert=True,
        is_icon_alert=True,
        is_upper_text_alert=True,
        is_lower_text_alert=True,
    )
    image = image_generator.generate_detailed_view_two_lines(
        detailed_view_two_lines_data
    )

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_detailed_view_two_lines_dark_mode_alert_yellow(config: Config):
    """Test the generate_detailed_view method."""

    config.color_mode = ColorMode.DARK
    config.color_palette = ColorPalette.YELLOW

    image_generator = ImageGenerator(config)

    detailed_view_two_lines_data = DetailedViewTwoLinesData(
        "media/waste/waste_large.png",
        "Restabfall",
        "In 2 Tagen",
        is_border_alert=True,
        is_icon_alert=True,
        is_upper_text_alert=True,
        is_lower_text_alert=True,
    )
    image = image_generator.generate_detailed_view_two_lines(
        detailed_view_two_lines_data
    )

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_dashboard_view_light_mode(config: Config):
    """Test the generate_dashboard_view method."""

    image_generator = ImageGenerator(config)

    dashboard_view_data = DashboardViewData(
        elements=[
            DashboardElementData(
                "media/waste/waste_small.png",
                "2 Tage",
            ),
            DashboardElementData(
                "media/waste/recycling_small.png",
                "14 Tage",
            ),
            DashboardElementData(
                "media/waste/paper_small.png",
                "Morgen",
                is_icon_alert=True,
            ),
            DashboardElementData(
                "media/waste/organic_small.png",
                "Heute",
                is_icon_alert=True,
                is_text_alert=True,
            ),
        ]
    )
    image = image_generator.generate_dashboard_view(dashboard_view_data)

    assert image is not None

    image.show()


@pytest.mark.skip()
def test_generate_dashboard_view_dark_mode(config: Config):
    """Test the generate_dashboard_view method."""

    config.color_mode = ColorMode.DARK

    image_generator = ImageGenerator(config)

    dashboard_view_data = DashboardViewData(
        elements=[
            DashboardElementData(
                "media/waste/waste_small.png",
                "2 Tage",
            ),
            DashboardElementData(
                "media/waste/recycling_small.png",
                "14 Tage",
            ),
            DashboardElementData(
                "media/waste/paper_small.png",
                "Morgen",
                is_icon_alert=True,
            ),
            DashboardElementData(
                "media/waste/organic_small.png",
                "Heute",
                is_icon_alert=True,
                is_text_alert=True,
            ),
        ],
        is_border_alert=True,
    )
    image = image_generator.generate_dashboard_view(dashboard_view_data)

    assert image is not None

    image.show()
