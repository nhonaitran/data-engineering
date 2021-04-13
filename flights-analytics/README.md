Flight Analytics

## Dataset
The flight dataset is composed of tab-delimited files called daystream file.
Each file represents all flights FlightAware tracked for a particular day.  The
daystream files are stored by year and by month.

Each line in the file is a flight event of a specific flight.  The flight event
can be one of the followings:
* flight scheduled
* flight filed
* avionics on
* flight off block
* ground position (taxiing)
* departed
* position
* arrived
* ground position (taxiing)
* on block
* avionics off


## Data Model

The flights information is captured in Flight table:
* id
* ident
* departure
* arrival
* status

Departure table:
* flight id
* airport
* departure time

Arrival table:
* flight id
* airport
* arrival time

Position table:
* flight id
* latitude
* longitude
* ground speed
* altitude

Airport table:
* id
* code
* type (icao/iata/lid)

## Data processing pipeline

The data extract-transform-load pipeline is comprised of three major components.of
an ETL workflow;
* the extractor,
* the annotator,
* the geojson generator, and
* web-based flights viewer


### The Extractor
The first component is the Extractor, a Spark distributed system that processes
the daystream files continuously and extracts the relevant attributes about the
flights tracked for that day.  It is responsible for keeping track of the flights
it has processed and group all the event messages for a flight together.

Once the flight is complete, it is written out to disk in a parquet format files.
The files are stored by origin airport to allow for parallal processing of the 
daystream files.

### The Annotator
While the majority of airline flights have origin and destination known, many
general aviation flights often do not have origin and destiation declared at the
time when the flights take off from its origin.

In those cases, we often store the latitude and longitude of the position when we
process the departure or arrival message for those flights.  Thus, we need to
determine the nearest airport to that lat/lon coordinates and annotate the message
with the guestimate airport code as origin or destination of that flight.

Once the airport code is found, the annotator updates the flight entity with the
new updated airport information that it has computed.

### The Geojson Generator
While is it often easier to use console or terminal to analyze the data while we
process it, the flights dataset is better visuallized with a full fledged 
visualization tool that shows the track path of the flights.

The data format that is easiest for most map-centric visualization tools is the
geojson data format.  The Goejson Generator ingests the annotated flight dataset
and converts the flight data into the geojson data which are then output into
disk.

### The Flights Viewer
Flights viewer is a web-based UI tool that users have access to online to view
flights data for specific timeframe.  