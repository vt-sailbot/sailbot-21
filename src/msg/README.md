# Messaging System

> Communication Layer between all separate processes... Allows for processes to interact with eachother while providing a level of separation

## consumer.c

### Functions

1. register_to_consume_data(int \<channelName>, void\* \<callback>)

```
Register with relay to consume data on channelName
Will now be called by notify_consumers upon data being published on channelName
```

2. data_callback(void \*\<dataPtr>)

```
Dereference data and pass to data_callback
data_callback will call a cython function, which will serve as an intermediary to the pyton data_callback
```

## producer.c

### Functions

1. register_to_produce_data(int \<channelName>, int \<dataSize>)

```
Register with relay to produce data on channelName
Producer and dataPtr to publishing address are stored in hashArray by relay
```

2. publish_data(int \<channelName>, int \<dataSize>, int \*\<sourcePtr>)

```
Receives sourcePtr to data and pushes it to shared memory
Notifies relay so that it can notify_consumers on this channel
```
 
## relay.c

### Functions

1. create_shared_memory(size_t \<size>)

```
Returns pointer to shared memory address which has been allocated to this producer
Called by create_buffer when new producer registers with the relay
```

2. search(int \<channelName>)

```
Searches hashArray and returns channelTable object according to channelName given if entry exists
```

3. delete(struct channelTable\* \<item>)

```
Removes channelTable entry from hashArray and replaces it with default values
```

4. insert_producer(int \<channelName>, int\* \<dataPtr>)

```
Makes entry into hashArray consisting of the channelName and dataPtr
Consumer field is set as NULL as a default value
```

5. insert_consumer(int \<channelName>, void\* \<consumer>)

```
Registers the consumer data callback with the channel
This entry will be found by notify_consumers and the callback will be called
```

6. notify_consumers(int \<channelName>, int\* \<dataPtr>)

```
Creates thread for each consumers data callback stored in channelTable
Thread creation not currently working, can still do callback just not multiprocessing-ly
```

7. display()

```
Creates visual representation of entire hashArray (doesn't show consumers)
```

8. display_consumers(int \<channelName>)

```
Creates visual representation of consumers for a given channelName
```
