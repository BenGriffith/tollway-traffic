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

While streaming data sources can be extremely complex, I tried to include controls allowing for different learning experiences such as handling of late events or duplicate events being delivered to a topic. Here is a list of the parameters and a high-level description of each one:

- `total_events` - number of events to generate
- `event_rate` - rate at which events should be created
- `output_file` - write all events to a local file/log
- `output_filename` - provide your own JSON filename
- `date_variation` - "mini-batch" of messages with noticeably different dates created in a short period of time
- `include_late` - meant to simulate scenario where events are pushed to a topic out of order
- `include_duplicate` - meant to simulate scenario where duplicate events are pushed to the same topic

Please note: `include_late` and `include_duplicate` can be used together, however, `date_variation` must be used by itself. It's either `date_variation` or `include_late` and `include_duplicate`.

## Installation
```
$
```
