#include <string.h>
#include <stdlib.h>

#define NO_COMPARTS 2

struct compart comparts[NO_COMPARTS] = {
    {.name = "struct compartment", .uid = 1000, .gid = 1000, .path = NULL},
    {.name = "other compartment", .uid = 1000, .gid = 1000, .path = NULL}
};

struct extension_data simple(struct extension_data data)
{
    fprintf(stderr, "simple called!\n");
    printf("DATA: %c\n", data.buf[0]);
    if (data.buf[0] == 'A') {
        fprintf(stderr, "data compared!");
        struct extension_data result;
        result.bufc = 1;
        result.buf[0] = 'B'; 
        fprintf(stderr, "Hello World!\n");
        return result;
    }
    else {
        fprintf(stderr, "[ERROR] data is not correct!\n");
        struct extension_data result;
        result.bufc = 0;
        bzero(result.buf, EXT_ARG_BUF_SIZE);
        return result;
    }
}
