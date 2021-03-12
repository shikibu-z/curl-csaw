#include <string.h>
#include <stdlib.h>
#include "urldata.h"
#include "multihandle.h"

#define NO_COMPARTS 2

static struct compart comparts[NO_COMPARTS] =
    {{.name = "struct compartment", .uid = 1000, .gid = 1000, .path = NULL},
     {.name = "other compartment", .uid = 1000, .gid = 1000, .path = NULL}};

struct extension_id *return_same_ext = NULL;

struct extension_data ext_check_data_to_resp(int result);

void _unmarshall_struct_Curl_easy(char *buf, size_t *buf_index_, struct Curl_easy **TEST_data);

void marshall_struct_Curl_easy(char *buf, size_t *buf_index_, struct Curl_easy *TEST_data);

void marshall_struct_Progress(char *buf, size_t *buf_index_, struct Progress *TEST_data);

void ext_check_data_from_arg(struct extension_data data, struct Curl_easy **ce);

int ext_check_data_from_resp(struct extension_data data);

struct extension_data ext_check_data_to_arg(struct Curl_easy *ce);

void _unmarshall_struct_Progress(char *buf, size_t *buf_index_, struct Progress **TEST_data);

struct extension_data ext_check_data(struct extension_data data);

#define unmarshall_struct_Curl_easy(a, b, c) _unmarshall_struct_Curl_easy(a, b, &c)

#define unmarshall_struct_Progress(a, b, c) _unmarshall_struct_Progress(a, b, &c)

#ifndef _LIBCOMPART_SERIALISATION__
#define _LIBCOMPART_SERIALISATION__

void unmarshall_string_(char *buf, size_t *buf_index_, char **str);
void marshall_string(char *buf, size_t *buf_index_, char *str);

#define MARSHALL_CAT_(a, b) a##b

#define MARSHALL_CAT(a, b) MARSHALL_CAT_(a, b)

#define unmarshall_string(buf, buf_index, str) unmarshall_string_(buf, buf_index, &str)

//only use for primitive data types
#define marshall_prim(buf, buf_index, data)                            \
  size_t MARSHALL_CAT(marshall, __LINE__) = sizeof(data);              \
  memcpy(&buf[*(buf_index)], &data, MARSHALL_CAT(marshall, __LINE__)); \
  *(buf_index) += MARSHALL_CAT(marshall, __LINE__);

#define unmarshall_prim(buf, buf_index, data)                          \
  size_t MARSHALL_CAT(marshall, __LINE__) = sizeof(data);              \
  memcpy(&data, &buf[*(buf_index)], MARSHALL_CAT(marshall, __LINE__)); \
  *(buf_index) += MARSHALL_CAT(marshall, __LINE__);

#define marshall_size(buf, buf_index, data, size)                     \
  size_t MARSHALL_CAT(marshall, __LINE__) = sizeof(data[0]) * size;   \
  memcpy(&buf[*(buf_index)], data, MARSHALL_CAT(marshall, __LINE__)); \
  *(buf_index) += MARSHALL_CAT(marshall, __LINE__);

#define unmarshall_size(buf, buf_index, data, size)                   \
  size_t MARSHALL_CAT(marshall, __LINE__) = sizeof(data[0]) * size;   \
  data = calloc(size, sizeof(data[0]));                               \
  memcpy(data, &buf[*(buf_index)], MARSHALL_CAT(marshall, __LINE__)); \
  *(buf_index) += MARSHALL_CAT(marshall, __LINE__);

#endif // _LIBCOMPART_SERIALISATION__

int check_data(struct Curl_easy *ce)
{
  if (ce->progress.current_speed != -1)
  {
    fprintf(stderr, "[RESULT] Current Speed: %ld\n", ce->progress.current_speed);
    return 1;
  }
  return 0;
}

//marshall string to [size][str]
void marshall_string(char *buf, size_t *buf_index_, char *str)
{
  size_t buf_index = *buf_index_;

  if (str)
  {
    //NULL terminate
    size_t str_length = strlen(str) + 1;
    memcpy(&buf[buf_index], &str_length, sizeof(str_length));
    buf_index += sizeof(str_length);

    memcpy(&buf[buf_index], str, str_length);
    buf_index += str_length;
  }
  else
  {
    memset(&buf[buf_index], 0, sizeof(size_t));
    buf_index += sizeof(size_t);
  }

  *buf_index_ = buf_index;
}

void unmarshall_string_(char *buf, size_t *buf_index_, char **str)
{
  *str = NULL;
  size_t buf_index = *buf_index_;

  size_t str_length = 0;
  memcpy(&str_length, &buf[buf_index], sizeof(str_length));
  buf_index += sizeof(str_length);

  if (str_length > 0)
  {
    //consider for NULL terminated
    *str = calloc(str_length, sizeof(char));
    memcpy(*str, &buf[buf_index], str_length);
    buf_index += str_length;
  }

  *buf_index_ = buf_index;
}
void _unmarshall_struct_Curl_easy(char *buf, size_t *buf_index_, struct Curl_easy **TEST_data)
{
  size_t size_of_element_ = 0;
  size_t buf_index = *buf_index_;
  unmarshall_prim(buf, &buf_index, size_of_element_);
  *TEST_data = NULL;
  if (size_of_element_)
  {
    *TEST_data = calloc(1, sizeof(**TEST_data));
    struct Curl_easy *TEST_data_ref = *TEST_data;
    {
      struct Progress *tmp = NULL;
      unmarshall_struct_Progress(buf, &buf_index, tmp);
      memcpy(&TEST_data_ref->progress, tmp, sizeof(*tmp));
      free(tmp);
    }
  }
  *buf_index_ = buf_index;
}

#define unmarshall_struct_Curl_easy(a, b, c) _unmarshall_struct_Curl_easy(a, b, &c)

void marshall_struct_Curl_easy(char *buf, size_t *buf_index_, struct Curl_easy *TEST_data)
{
  size_t buf_index = *buf_index_;
  if (TEST_data)
  {
    size_t size_of_element_ = sizeof(*TEST_data);
    marshall_prim(buf, &buf_index, size_of_element_);
    marshall_struct_Progress(buf, &buf_index, &TEST_data->progress);
  }
  else
  {
    size_t size_of_element_ = 0;
    marshall_prim(buf, &buf_index, size_of_element_);
  }
  *buf_index_ = buf_index;
}
void marshall_struct_Progress(char *buf, size_t *buf_index_, struct Progress *TEST_data)
{
  size_t buf_index = *buf_index_;
  if (TEST_data)
  {
    size_t size_of_element_ = sizeof(*TEST_data);
    marshall_prim(buf, &buf_index, size_of_element_);
    marshall_prim(buf, &buf_index, TEST_data->current_speed);
  }
  else
  {
    size_t size_of_element_ = 0;
    marshall_prim(buf, &buf_index, size_of_element_);
  }
  *buf_index_ = buf_index;
}
void _unmarshall_struct_Progress(char *buf, size_t *buf_index_, struct Progress **TEST_data)
{
  size_t size_of_element_ = 0;
  size_t buf_index = *buf_index_;
  unmarshall_prim(buf, &buf_index, size_of_element_);
  *TEST_data = NULL;
  if (size_of_element_)
  {
    *TEST_data = calloc(1, sizeof(**TEST_data));
    struct Progress *TEST_data_ref = *TEST_data;
    unmarshall_prim(buf, &buf_index, TEST_data_ref->current_speed);
  }
  *buf_index_ = buf_index;
}

#define unmarshall_struct_Progress(a, b, c) _unmarshall_struct_Progress(a, b, &c)

struct extension_data ext_check_data_to_resp(int result)
{
  struct extension_data data;
  char *buf = data.buf;
  size_t buf_index = 0;
  marshall_prim(buf, &buf_index, result);
  data.bufc = buf_index;
  return data;
}
void ext_check_data_from_arg(struct extension_data data, struct Curl_easy **ce)
{
  char *buf = data.buf;
  size_t buf_index = 0;
  unmarshall_struct_Curl_easy(buf, &buf_index, *ce);
}
int ext_check_data_from_resp(struct extension_data data)
{
  int result;
  char *buf = data.buf;
  size_t buf_index = 0;
  unmarshall_prim(buf, &buf_index, result);
  return result;
}
struct extension_data ext_check_data_to_arg(struct Curl_easy *ce)
{
  struct extension_data data;
  char *buf = data.buf;
  size_t buf_index = 0;
  marshall_struct_Curl_easy(buf, &buf_index, ce);
  data.bufc = buf_index;
  return data;
}
struct extension_data ext_check_data(struct extension_data data)
{
  struct Curl_easy *ce;
  ext_check_data_from_arg(data, &ce);
  int return_value;
  return_value = check_data(ce);
  struct extension_data result = ext_check_data_to_resp(return_value);
  return result;
}
