 
* TOC
{:toc} 

# `co2eq` Overview

`co2eq` estimates the CO2 equivalent (CO2eq) of air flight and is especially targeting international meetings. 

The main advantage of `co2eq` is that is provides a realistic estimation of the CO2eq by flying from A to city B. 

1. CO2eq is highly dependent on the number of connections, and travel journey. To address this `co2eq` leverages [Amadeus API](https://developers.amadeus.com/get-started/get-started-with-amadeus-apis-334) to retrieve a __realistic flight__ that may be __a direct flight__ or composed of __multiple segments__. 
2. `co2eq` estimates the emission for each segments implementing different methodologies such as [myclimate](https://www.myclimate.org/), the one provided by the [UK government](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1049346/2021-ghg-conversion-factors-methodology.pdf) [WEB](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2021) or the online service proposed by [GoClimate](https://www.goclimate.com/).  
3. Flight origin or destination are identified with IATA codes and are usually not provided. `co2eq` provides means to bind the provided location to the IATA code. In our case, the location is mostly described by a Country name or ISO Code.  

More documentation is available on `co2eq`:

* [CO2eq: "Estimating Meetings' Air Flight CO2eq - An Illustrative Example with IETF meetings](https://www.iab.org/wp-content/IAB-uploads/2021/11/Migault.pdf) provides a more detailed description of the methodology.
* [co2eq-IETF](https://mglt.github.io/co2eq/IETF/IETF/) and [co2eq-ICANN](https://mglt.github.io/co2eq/ICANN/ICANN/) show `co2eq` outputs for IETF and ICANN meetings.

# Using `co2eq` 

The `co2eq` package contains a few command lines.

`co2eq-get-flight` returns a realistic flight from Los Angeles (LAX) to Paris (PAR). In the example below, the flight consisted of 4 segment flight and the corresponding emissions are 3081 kg (resp. 3900 kg) when estimated with myclimate  (resp. goclimate). 

```
co2eq-get-flight LAX PAR
  {
  "origin": "PAR",
  "destination": "LAX",
  "departure_date": "2021-11-18",
  "return_date": "2021-11-25",
  "cabin": "ECONOMY",
  "adults": 1,
  "segment_list": [
    [
      "CDG",
      "FRA"
    ],
    [
      "FRA",
      "LAX"
    ],
    [
      "LAX",
      "YUL"
    ],
    [
      "YUL",
      "CDG"
    ]
  ],
  "price": "719.98",
  "currency": "EUR",
  "travel_duration": "1 day, 5:50:00",
  "flight_duration": "1 day, 0:53:00",
  "co2eq": {
    "myclimate": 3081.790499572582,
    "goclimate": 3900.0
  }
}
```

For international meetings, we generally do not know the exact origin of each attendee, but in many case we know the country of origin and the (exact) closest airport of the meeting. 
`co2eq-plot-meeting` estimate the origin of the participant. In general the participant is considered flying from the capital of the country, but in some cases, the capital is not the most important city. In addition, in the US, we split attendees between Est and West coast, to better reflect the air flight distance. 

If ietf72.json.gz lists the participants of the meeting IETF72, various representations of the estimation of the CO2 can be generated as follows:

```
co2eq-plot-meeting   --output_dir  ./output --meeting_name IETF72 --meeting_attendee_list ./ietf72.json.gz --meeting_location_iata 'DUB'
```

The attendee list is stored in ietf72.json.gz as follows:

```
[
  {
    "country": "US",
    "organization": "Cisco",
    "presence": "on-site"
  },
  {
    "country": "FR",
    "organization": "Nokia",
    "presence": "remote"
  },
  {
    "country": "US",
    "organization": "Google",
    "presence": "on-site"
  },
  {
    "country": "IN",
    "organization": "indian career welfare society",
    "presence": "remote"
  },
  {
    "country": "JP",
    "organization": "japan registry services co., ltd.",
    "presence": "on-site"
  }
]
```

Note that as, this package is maintained for IETF and ICANN meetings, `co2eq-plot-meeting   --output_dir  ./output --meeting_name IETF72` is sufficient.

In addition, international meetings often consist in a series of meetings. Typically IETF and ICANN meetings occur 3 time a year.   
The series of meetings (including all individual meetings) is plot as follows:

```
co2eq-plot-meeting   --output_dir  ./output --meeting_list_conf meeting_list_conf.json.gz
```

where meeting_list_conf.json.gz contains all information related to the meetings:

```
{
  "name": "IETF",
  "meeting_list": [
    {
      "name": "IETF72",
      "location": {
        "country": "IE",
        "city": "Dublin"
      },
      "attendee_list": "ietf/meeting_attendee_list/json/ietf72.json.gz"
    },
    {
      "name": "IETF73",
      "location": {
        "country": "US",
        "city": "Minneapolis"
      },
      "attendee_list": "ietf/meeting_attendee_list/json/ietf73.json.gz"
    },
   ...
```

Note that for IETF and ICANN meeting, these pieces of information are provided by the package and `co2eq-plot-meeting   --output_dir  ./output --meeting_template IETF` is sufficient. 

# Installation 

Installation of `co2eq` can be done directly via pip.

```bash
pip3 install co2eq
```
The development of `co2eq` have lead to the data of the country_info package to be updated. Before this modification being released in the country_info release, the updated version of country_info can be installed as follows:

```bash
git clone https://github.com/mglt/countryinfo
cd country_info
python3 setup.py install
To compute the CO2 using GO Climate service, the climate neutral package needs to be installed.
```

```bash
git clone https://github.com/mglt/climate_neutral
cd climate_neutral
sudo python3 setup.py install
```

## Local installation

For installing `co2eq` in a python virtual environment
```bash
$ pip3 install virtualenv       # If you do not have virtualenv installed
$ python3 -m virtualenv co2eq   # Create a bew virtual environment
$ source co2eq/bin/activate     # Activate the virtual environment 
```
# Configuring `co2eq`

The ~/.config/co2eq directory contains the configurations files. 

* the `env` file that contains the different login/passwords to connect to [AMADEUX](https://developers.amadeus.com/get-started/get-started-with-amadeus-apis-334) or [GoClimate](https://api.goclimate.com/docs)
* the ISO3166_REPRESENTATIVE_CITY that enables to match a country code with a specific IATA airport code.  

These files are provided in the `conf` directory of the git repo.

We also provide the cache to provision your cache - and avoid some request to be made. It is very unlikely that this will satisfy your need, but that can be useful for testing for example or reduce the requests. The cache content is available under the `cache` directory of the `co2eq` [git repository](https://github.com/mglt/co2eq/tree/main).

The `env` file is as described below:

```
## The directory where air flights, or CO2 emissions for a given air flight
## requested to GO Climate are stored after it has been requested.
## The main purpose if to prevent co2eq to resolve the same request multiple time
CACHE_DIR = "~/.cache/co2eq"

## co2eq retrieves flight offers to estimate a real flight and uses the AMADEUS API:
## https://developers.amadeus.com/get-started/get-started-with-amadeus-apis-334
## You need to register and request and an API Key and an API Secret for the
## Flight Offers Search service.
AMADEUS_ID = 'XXXXXXXXXXXXXXXXXXXXXXXX'
AMADEUS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXX'

## To compute the CO2 emissions associated a flight a request is sent to GO Climate
## Please go through https://api.goclimate.com/docs to get an account.
GOCLIMATE_SECRET =  'XXXXXXXXXXXXXXX'
NOMINATIM_ID = "ietf"

## where logs are stored. We suggest you perform tail -f your_log_file
## to monitor what can possibly go wrong.
log = '/tmp/co2eq.log'

## CityDB specific parameters
## ISO3166_REPRESENTATIVE_CITY enable to indicate a specific
## representative city for that country.
## This is usually useful when the capital is not the main 
## representative city or when no flight can be retrieved from 
## that country
ISO3166_REPRESENTATIVE_CITY = '~/.config/co2eq/ISO3166_REPRESENTATIVE_CITY.json.gz
```

Optionally the `ISO3166_REPRESENTATIVE_CITY.json.gz` contains mapping between a ISO country code and a specific city. This is essentially when the standard mapping between the ISO country code and the largest airport does not provide a flight. In many cases, this is likely due to the limitation of the Amadeus API - as we are using the free version. 

```
{
  "IL": {
    "name": "Tel Aviv Yafo",
    "iata": "TLV"
  },
  "PS": {
    "name": "Tel Aviv Yafo",
    "iata": "TLV"
  },
  "AU": {
    "name": "Sydney",
    "iata": "YQY"
  },
  "NZ": {
    "name": "Auckland",
    "iata": "AKL"
  },
  "CY": {
    "name": "Larnaca",
    "iata": "LCA"
  },
  "CH": {
    "name": "Zurich",
    "iata": "ZRH"
  },
  "ZA": {
    "name": "Johannesburg",
    "iata": "JNB"
  },
  "CI": {
    "name": "Abidjan",
    "iata": "ABJ"
  },
  "SK": {
    "name": "Kosice",
    "iata": "KSC"
  },
  "BO": {
    "name": "Sao Paulo",
    "iata": "SAO"
  },
  "CA": {
    "name": "Toronto",
    "iata": "YTO"
  },
...
]
```

# Special use: `co2eq` for IETF and ICANN meeting

This section details how to use `co2eq` to display CO2eq for IETF and ICANN. 
The results are respectively published [co2eq-IETF](https://mglt.github.io/co2eq/IETF/IETF/) and [co2eq-ICANN](https://mglt.github.io/co2eq/ICANN/ICANN/).

## `co2eq-get-attendee-list`

co2-attendee-list is a tool to output the attende-list into an appropriated format for co2eq.
The current `txt` template enables to output json files out of the following files:
These is the format we use to convert files we receive from ICANN.

```
Japan   680
United States of America        372
United Kingdom of Great Britain and Northern Ireland    44
Canada  41
Australia       38
Germany 38
Belgium 29
...
```  
The json attendee list are output as follows:

```
co2eq-get-attendee-list --template txt icann64_KIX.txt 

```

By default the output file is icann64_KIX.json.gz, that is to say the same as the input_file with a different extensions allocated in the same directory.


The IETF attendee list are collected from the IETF website.

```
co2eq-get-attendee-list ietf114 
co2eq-get-attendee-list --template ietf ietf114 
```
By default the output file is ./ietf114.json.gz but you can specify the specific output file as follows:

## `co2eq-plot-meeting`

The `co2eq-plot-meeting` displays the COeq emissions for the meetings. It enables to plot a single meeting or the CO2 emissions for a serie of meetings.
The package contains the data for IETF and ICANN meeting, that is the package co2eq provided the list of attendees as well as the location associated to each meetings. As a result, these argument do not need to be provided. 

To plot a specific meeting in this example ICANN55:
 
```
co2eq-plot-meeting --output_dir  ./output_test/ --meeting_type ICANN --meeting_name ICANN55
co2eq-plot-meeting --output_dir  ./output_test/ --meeting_name ICANN55
```
This will result in :

```
  output_test
    +- ICANN55 
```

To plot all ICANN meetings:

```
co2eq-plot-meeting --output_dir  ./output_test --meeting_type ICANN 
co2eq-plot-meeting --output_dir  ./output_test --meeting_name ICANN
```

```
  output_test
    +- ICANN 
    +- ICANN55
    +- ...
    +-ICANN76 
```


To generate all our web site

```
co2eq-plot-meeting --output_dir  ./IETF --meeting_type IETF 
co2eq-plot-meeting --output_dir  ./ICANN --meeting_type ICANN
```

As a developer, this is how to update the co2eq package and generate an additional IETF meeting for example

```
## 1. configure package with new data
## vim co2eq/src/co2eq/data/meeting_list_conf.json.gz
## 2. generates the attendee_list for that IETFXX
cd co2eq/src/co2eq/data/ietf/meeting_attendee_list/json/
co2eq-get-attendee-list ietfXXX 
## 3. update package
cd co2eq/
python3 -m build && pip3 install --force-reinstall  dist/co2eq-0.0.4.tar.gz
## git branch gh-pages
## 4. plot the new graph and generate the web site
co2eq-plot-meeting --output_dir  ./IETF --meeting_type IETF 
``` 

Without updating the package 

```
## 1. generates the attendee_list for that IETFXX
co2eq-get-attendee-list ietfXX
## 2) generates meeting_list_conf.json.gz by adding
## {'name' : 'IETFXX',
##    'location' : {
##      'country' : 'Country',
##      'city' : 'City',
##      'iata' : 'IATA' },
##    'attendee_list' : './ietfXX.json.gz'
##  }
co2eq-plot-meeting --output_dir  ./IETF --meeting_type IETF --meeting_list_conf meeting_list_conf.json.gz 
```

# Special Use: Netlifying `co2eq` [Live App](https://co2eq.netlify.app) Deployment Status:&nbsp; [![Netlify Status](https://api.netlify.com/api/v1/badges/d8891a86-be1d-4e5a-8789-b4592385910a/deploy-status)](https://app.netlify.com/sites/co2eq/deploys)

## Running docker container (examples/docker)

```bash
$ docker build --tag co2eq .      # Build the image using Docker
$ docker run -p8000:8000 co2eq    # Run the Docker image
```

## Running the frontend

To run the frontend, open [src/frontend/index.html](src/frontend/index.html) on your browser.

If you are running the server on your local machine or a different remote server, make sure to update the backend URL in the [src/frontend/index.html](src/frontend/index.html) file. Change [const socketUrl="ws://..."](https://github.com/pssingh21/co2eq/blob/68983eb8c7506031cb830c9e6989fca2e2028db9/src/frontend/index.html#L325) to your backend URL.

## Deploying the application

To deploy the backend, build the Docker image and push the image to the server. 
To deploy the frontend, upload the [examples/docker/frontend/index.html](/frontend/index.html) file to the server.

## JSON format for the web interface
Format of JSON file to upload via frontend:
```json
{ 
    "name" : "required", 
    "location" : { 
        "country" : "required", 
        "iata": "optional"
    },
    "attendee_list": [
        {
            "country": "required",
            "iata": "optional",
            "number_of_attendee": required
        }
    ]                                    
}
```
Example:
```json
{ 
    "name" : "meeting_201", 
    "location" : { 
        "country" : "DE", 
        "iata": "SXF"
    },
    "attendee_list": [
        {
            "country": "US",
            "iata": "LAX",
            "number_of_attendee": 1
        },
        {
            "country": "FR",
            "number_of_attendee": 2
        },
        {
            "country": "JP",
            "number_of_attendee": 5
        }
    ]                                    
}

```

## JSON Format for web service (typically the one used for MeetingList)
Format of data to be sent to API endpoint:
```json
{ 
    "name" : "required", 
    "location" : { 
        "country" : "required", 
        "iata": "optional"
    },
    "attendee_list": [
        {
            "country": "required",
            "iata": "optional"
        }
    ]                                    
}
```
Example:
```json
{ 
    "name" : "meeting_201", 
    "location" : { 
        "country" : "DE", 
        "iata": "SXF"
    },
    "attendee_list": [
        {
            "country": "US",
            "iata": "LAX",
        },
        {
            "country": "FR"
        },
        {
            "country": "FR"
        },
        {
            "country": "JP"
        }
    ]                                    
}

```




# Contributors: 

* Peeyush Man Singh ([pssingh21](https://github.com/pssingh21)) Dockerized and implemented co2eq as a web service, with web interface and backend service. An example of the service is available here: https://co2eq.netlify.app/ as well as in example/docker. He also integrate the use of a configuration file .env


# TODO:

1. The output figures should probably distinguish the estimation of the CO2eq from remote attendee and on-site attendee. This is especially useful when cluster_key is different from presence.
  * this probably requires to standardize the key word "presence"
  * outsource the plot histogram to a dedicated class with a well defined json input file.
2. `co2eq` computes CO2eq per passenger per Km in a relative indepednent way. this should probably integrated when the co2eq emission are computed for each users.
3. Speed up the computation: The overall process is quite slow - even with the presence of cache. We need to check what is really happening. It could be a lot of read, open file operations. Maybe also having a real database may help.
   
