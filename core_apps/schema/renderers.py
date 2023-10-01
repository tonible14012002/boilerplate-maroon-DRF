from rest_framework.renderers import JSONRenderer


class MyJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        '''
        Format non-pageable api endpoint
        '''
        status_code = renderer_context['response'].status_code
        formated_data = data

        if not (
            hasattr(data, '__iter__')
            and ("data" in data and "pageable" in data)
        ):
            formated_data = {
                'pageable': None,
                'data': data
            }

        formated_data['status_code'] = status_code
        return super().render(formated_data, accepted_media_type, renderer_context)

# EXAMPLE SCHEMA FOR RETURNING RESPONSE DATA
# {
#     # null if not pageable
#     pageable: {
#         page: number # number of page
#         size: number # size of current list
#         next: number | null # next page number
#         previous: number | null # previous page number
#     },
#     data: # actual data returned by a view
# }
