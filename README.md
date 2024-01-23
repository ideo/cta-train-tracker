# CTA Train Tracker API
A python wrapper built for our interactive LED L Map!

### Usage
To query for all CTA train locations data and print it to the screen, run:
```bash
python -m get_train_locations
```

To simply the results to just the latitude and longitude of each train and to write the output to a JSON file, run:
```bash
python -m get_train_locations --simplify --json
```

I used Poetry to develop this, so I run `poetry run python ...` for each of these commands.


### Development
- python 3.11.6
- Poetry
- [CTA Train Tracker API Documentation](https://www.transitchicago.com/developers/ttdocs/)


