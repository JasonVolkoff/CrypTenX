-   Will we need two entirely separate logic bots? (one to generate entry/exit, one to examine performance with logic generated from the first bot?)

## Data Gathering bot

-   Gather a few years worth of historical data & save to DB along (ensure a datetime exists; this will be used to order-by date later)
-   Will take an optional two dates as input (at least one is REQUIRED)

#### Input validation

-
-   If nothing is in the database: two dates are REQUIRED; else throw error
-   If the database has values stored: one date REQUIRED; throw error if more or less is given
-   If one date is given && the database has values stored:
    -   Check if date is before OR after the dates stored in DB; throw error if date exists between what is already stored...
    -   If date is BEFORE: work BACKWARDS from oldest date value & begin storing entries until BEFORE date is reached (or API limit is hit)
    -   If date is AFTER: work FORWARDS from most recent date value & begin storing entries until AFTER date is reached (or API limit is hit)
-   Technically, we could configure a range to indicate space between calls, but we can keep this a static 5 minute interval...
-   We could also consider adding additional API calls from other sources: this could be saved to each model entry as additional (nullable) fields, OR as a (nullable) one-to-one

#### Scaling

-   Once parameter bot is configured appropriately, we can use a cron-job to run the data gathering bot in real time, then send signals for entry/exits.
-   These signals could be in the form of notifications to the user OR direct buy/sells on an active account (if this option is pursued, the parameter bot will need to be
    configured to account for fees)

## Parameter Bot (should this double as validation?)

#### RETURN VALUE

Inital thoughts:

-   Ideally, the return value generates metrics to determine an entry strategy, plus an exit strategy
-   These entry/exit strategies could be in the form of special values (such as a DELTA), or specific variables such as a percentage gain/drop over a period of time (i.e. if the value goes up by 5% within a 3 hour period, that indicates an exit point).
-   If we use this to double as validation, we'll need a REQUIRED starting dollar amount and will return details about our ending value.
-   This return value is to be saved within a model instance to generate a "profile" based on the logic (below).
-   Values Returned: Entry/Exit indicators
-

#### Logic

-   This process will most definitely entail an iteration of the entire saved database

##### Potential input variables:

-   Moving average timeframe (i.e in minutes/hours/days)

##### Potential business logic variables:

-   Price Moving Average: (Sum of all data points within moving average timeframe) / (# of data points)
-   Price Deviation: Current value - Moving Average
-   Price Variance: (((All datapoints within moving average timeframe) - (Moving Average)) ^ 2) / (# of data points)
-   Price Standard Deviation: sqrt(Variance)
-   Price Volitility: a weighted 0-1 DECIMAL that describes the current confidence in how stable the coin is (as iterations occur)
    -   Calculation: Avg of moving value timeframe
-   Volume Moving Average: Same as Price
-   Volume Deviation: Same as Price
-   Volume Variance: Same as Price
-   Volume Standard Deviation: Same as Price
-   Volume Volitilaty: Same as Price
-

##

## Models

-   Data model: this will store a representation of data gathered from cryptowatch API endpoint calls; we'll store one entry for every 5 minutes
-   Return value model: this will essentially store the return value generated from the parameter bot. All fields will need to be blankable/nullable, as we'll be trying many different parameter bots

-   datetime:

```
    from django.utils.timezone import make_aware
    from datetime import date
    close_time = 1474732800
    datetime_obj_with_tz = make_aware(datetime.fromtimestamp(close_time))
    EtheriumData.objects.create(close_time=close_time)
```
