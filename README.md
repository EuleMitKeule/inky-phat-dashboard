# Inky pHat Dashboard

## Configuration

Example `config.yml` to be created in the repo root directory:

```yaml
home_assistant:
  sensors:
    - entity_id: sensor.restabfallsammlung
      friendly_name: Restabfall
      name: waste
      icon_path_large: media/waste/waste_large.png
      icon_path_small: media/waste/waste_small.png
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
  token: <ha_token>
  url: <ha_url>
logging:
  level: INFO
color_palette: RED
waste_detailed_days: 1
waste_alert_days: 2
enable_inky: True
flip_screen: True
data_timeout_seconds: 20
view_change_interval_seconds: 60
```

## Development

This package can only be installed and run on a Linux OS or WSL.

1. Install [`poetry`](https://python-poetry.org/) (This will later be changed to [`uv`](https://docs.astral.sh/uv/))
2. Install dependencies with `poetry install`
3. Create a `config.yml` in the repository root
4. Run with `poetry run python inky_phat_dashboard/__main__.py`

To implement new layouts, `image_generator.py` can be extended with new image generation methods and `models.py` with new `ViewData` subclasses.
New modules can be implemented by subclassing `BaseModule` from `base_module.py` and implementing the abstract methods.
