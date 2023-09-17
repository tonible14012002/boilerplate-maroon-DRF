from rest_framework.renderers import JSONRenderer


class MyJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        '''
        Format non-pageable api endpoint
        '''
        formated_data = data
        if not ("data" in data and "pageable" in data):
            formated_data = {
                'pageable': None,
                'data': data
            }
        return super().render(formated_data, accepted_media_type, renderer_context)

# SCHEMA FOR RETURNING RESPONSE DATA
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
