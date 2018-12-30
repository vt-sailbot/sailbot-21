import pickle


cdef extern from "publisher.h":
    ctypedef struct Relay:
        pass
    void publish(Relay* relay, char* channel_name, void* data, size_t data_size)


def _publish(relay, channel_name, data):
    """Publishes data to a channel.

    Keyword arguments:
    channel_name -- The name of the channel to publish to
    data -- The data to send along the channel
    """
    pickled_data = pickle.dumps(data)

    cdef size_t data_size = <int>sizeof(pickled_data)
    cdef void* data_ptr = <void*>pickled_data

    publish(<Relay*>relay.relay, channel_name, data_ptr, data_size)
