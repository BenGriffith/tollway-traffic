## General Info

The purpose of Tollway Traffic is to simulate the generation of streaming data that can be used for learning purposes.

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
```
$ pip install tollway-traffic
```

## Setup


## Running
For usage and options/parameters detail
```
$ python -m tollway --help
```

Using `--total-events` generate 100 events
```
$ python -m tollway --total-events 100
```

Using `--total-events` and `--event-rate` generate 500 events at a rate of 50 milliseconds
```
$ python -m tollway --total-events 500 --event-rate 0.05
```

Using `--total-events` and `--output-file` generate 250 events and log each event to a local file
```
$ python -m tollway --total-events 250 --output-file
```

Using `--total-events` generate 10,000 events and enable `--date-variation`
```
$ python -m tollway --total-events 10000 --date-variation
```

Using `--total-events` generate 20,000 events and enable `--include-late` along with `--include-duplicate`
```
$ python -m tollway --total-events 20000 --include-late --include-duplicate
```

To enable `--pubsub`
```
$ python -m tollway --total-events 100 --pubsub
```
