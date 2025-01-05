# Inky pHat Dashboard

## Configuration

Example `config.yml` to be created in the repo root directory:

```yaml
home_assistant:
  sensors:
    - entity_id: sensor.restabfallsammlung  # The entity id of the sensor entity for this waste type
      friendly_name: Restabfall  # The name to display on screen for this waste type
      name: waste  # The id for this waste type (used internally)
      icon_path_large: media/waste/waste_large.png  # The icon to use when this waste type is shown in the detailed view
      icon_path_small: media/waste/waste_small.png  # The icon to use when this waste type is shown in the overview
    - entity_id: sensor.wertstoffsammlung
      friendly_name: Wertstoffe
      name: recycling
      icon_path_large: media/waste/recycling_large.png
      icon_path_small: media/waste/recycling_small.png
    - entity_id: sensor.altpapiersammlung
      friendly_name: Altpapier
      name: paper
      icon_path_large: media/waste/paper_large.png
      icon_path_small: media/waste/paper_small.png
  token: <ha_token>  # Long lived access token for Home Assistant
  url: <ha_url>  # Full url for your Home Assistant installation (e.g. https://home.example.com)
logging:
  level: INFO
color_palette: RED  # RED or YELLOW depending on your inky display
waste_detailed_days: 1  # Detailed screens for waste types are shown when they are due tomorrow
waste_alert_days: 2  # Waste types are displayed in red color when they are due in two days
enable_inky: True  # An inky display is attached to this device
flip_screen: True  # Flip = True means up is where the USB ports on the Pi Zero are
data_timeout_seconds: 20  # Timeout between data polling from Home Assistant
view_change_interval_seconds: 60  # Timeout between screen changes
```

## Development

This package can only be installed and run on a Linux OS or WSL.
When developing on a device that does not have an inky display attached, `enable_inky` has to be set to `False` in the `config.yml`.

1. Install [`poetry`](https://python-poetry.org/) (This will later be changed to [`uv`](https://docs.astral.sh/uv/))
2. Install dependencies with `poetry install`
3. Create a `config.yml` in the repository root
4. Run with `poetry run python inky_phat_dashboard/__main__.py`

To implement new layouts, `image_generator.py` can be extended with new image generation methods and `models.py` with new `ViewData` subclasses.
New modules can be implemented by subclassing `BaseModule` from `base_module.py` and implementing the abstract methods.
New configuration options are introduced by defining them in the `Config` class from `models.py`.
