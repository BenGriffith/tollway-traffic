## General Info

The purpose of Tollway Traffic is to simulate the generation of streaming data that can be used for various/learning purposes.

In the United States, when entering a tollway cameras will take a picture of each vehicle's license plate, and that information is used to identify the registered owner of the vehicle along with vehicle metadata such as make, model, year, category, color or VIN.

Tollway traffic generates a payload made up of the following properties:

- `year` - vehicle year
- `make` - vehicle manufacturer (e.g. Toyota, Honda, BMW)
- `model` - vehicle model (e.g. Land Cruiser, Civic, M5)
- `category` - vehicle category (e.g. Coupe, SUV, Sedan)
- `license_plate` - vehicle license plate
- `vin` - vehicle identification number
- `state` - vehicle state
- `primary_color` - vehicle color
- `tollway_state` - state of the tollway
- `tollway_name` - name of the tollway
- `timestamp` - timestamp for when vehicle entered tollway

Each payload is meant to represent an event of the process defined earlier. `Faker` is used to generate vehicle information while a web scraper is used to fetch names of tollways in each state/territory within the United States.

While streaming data sources can be extremely complex, I tried to include controls allowing for different scenarios such as the handling of late events or duplicate events being delivered to a topic. Here is a list of the parameters and a high-level description of each one:

- `--total-events` - number of events to generate
- `--event-rate` - rate at which events should be created
- `--output-file` - write all events to a local file/log
- `--output-filename` - provide your own JSON filename
- `--date-variation` - "mini-batch" of events with noticeably different dates created in a short period of time
- `--include-late` - meant to simulate scenario where events are pushed to a topic out of order
- `--include-duplicate` - meant to simulate scenario where duplicate events are pushed to the same topic
- `--pubsub` - push events to pubsub topic

Please note: when `--date-variation` is enabled `--include-late` and `--include-duplicate` must be disabled.

## Installation
1. Create virtual environment
```
$ python -m virtualenv .venv
```

2. Activate virtual environment
```
$ source .venv/bin/activate # Mac/Linux
$ .venv\Scripts\activate # Windows
```

3. Install dependencies
```
$ pip install -r requirements.txt
```

4. (Optional) Copy .env-template
```
$ cp .env-template .env
```

5. (Optional) Configure environment variables in `.env`

Five environment variables are already defined but they can be changed. `DATE_VARIATION_RATE`, `DATE_VARIATION_MIN` and `DATE_VARIATION_MAX` are implemented when `--date-variation` option is enabled. Similarly, `INCLUDE_LATE_RATE` is in use when `--include-late` is enabled and `INCLUDE_DUPLICATE_RATE` is applied when `--include-duplicate` is enabled.

- `DATE_VARIATION_RATE` controls how often events with older dates are generated.
- `DATE_VARIATION_MIN` and `DATE_VARIATION_MAX` are used to define range of integers that will be randomly selected from. The selected integer is then used to create a date in the past.
- `INCLUDE_LATE_RATE` controls the late event generation rate so, for example, for every 20 events one late event will be generated.
- `INCLUDE_DUPLICATE_RATE` controls the duplicate event generation rate so, for example, for every 50 events one duplicate event will be generated.
- `ALL_EVENTS_COUNT` is used to track events generated/for logging purposes.

6. (Optional) Enable pubsub functionality

To leverage delivery of events to pubsub as-is, the following pre-requisites are needed:

- Google Cloud Project
- Create service account for pubsub
    - Download service account key
    - Change filename to `pubsub.json` or easy to use
    - Move file to `service_account/` directory
- Terraform installed [follow link](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

Next, provide values for the following environment variables:

- `PROJECT_ID` - Google Cloud Project ID
- `TOPIC_ID` - Name of pubsub topic
- `PUBSUB_SERVICE_ACCOUNT` - Path to pubsub service account key such as `/service_account/pubsub.json`
- `GOOGLE_REGION` - Name of Google Geographical Region


[ADD MAKEFILE and REVIEW Installation steps]


## Running
For usage and options/parameters detail
```
$ python3 -m tollway --help
```

Using `--total-events` generate 100 events
```
$ python3 -m tollway --total-events 100
```

Using `--total-events` and `--event-rate` generate 500 events at a rate of 50 milliseconds
```
$ python3 -m tollway --total-events 500 --event-rate 0.05
```

Using `--total-events` and `--output-file` generate 250 events and log each event to a local file
```
$ python3 -m tollway --total-events 250 --output-file
```

Using `--total-events` generate 10,000 events and enable `--date-variation`
```
$ python3 -m tollway --total-events 10000 --date-variation
```

Using `--total-events` generate 20,000 events and enable `--include-late` along with `--include-duplicate`
```
$ python3 -m tollway --total-events 20000 --include-late --include-duplicate
```

To enable `--pubsub`
```
$ python3 -m tollway --total-events 100 --pubsub
```
