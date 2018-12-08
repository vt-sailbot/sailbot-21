#include <pthread.h>

#include "circular_buffer.h"


// Globals

pthread_mutex_t* mutex;


// Functions

CircularBuffer* init_circular_buffer() {
    CircularBuffer* new_buffer = (CircularBuffer*)malloc(sizeof(CircularBuffer));
    new_buffer->size = 0;
    new_buffer->head = 0;
    new_buffer->tail = 0;

    pthread_mutexattr_t* pthread_mutexattr;
    pthread_mutexattr_init(pthread_mutexattr);
    pthread_mutex_init(mutex, pthread_mutexattr);

    return new_buffer;
}


CircularBufferElement circular_buffer_push(CircularBuffer* buffer, Data* data) {
    pthread_mutex_lock(mutex);

    int next_index = buffer->size == 0 ? 1 : (buffer->head + 1) % MAX_BUFFER_SIZE;

    buffer->data[next_index] = *data;

    buffer->head = next_index;
    buffer->tail = (buffer->head - buffer->size + 1) % MAX_BUFFER_SIZE;

    if (buffer->size < MAX_BUFFER_SIZE) {
        buffer->size++;
    }

    if (next_index == 0) {
        buffer->revolutions++;
    }

    CircularBufferElement element;
    element.index = next_index;
    element.revolution = buffer->revolutions;

    pthread_mutex_unlock(mutex);
}


Data* circular_buffer_get_element(CircularBuffer* buffer, CircularBufferElement* elem) {
    pthread_mutex_lock(mutex);

    if (elem->index <= buffer->head && buffer->revolutions != elem->revolution) {
        return (Data*)NULL;
    }

    pthread_mutex_unlock(mutex);

    return &buffer->data[elem->index];
}


void empty_circular_buffer(CircularBuffer* buffer) {
    pthread_mutex_lock(mutex);

    buffer->size = 0;
    buffer->head = 0;
    buffer->tail = 0;

    pthread_mutex_unlock(mutex);
}


void destroy_circular_buffer(CircularBuffer** buffer) {
    free(*buffer);
    *buffer = (CircularBuffer*)NULL;
}