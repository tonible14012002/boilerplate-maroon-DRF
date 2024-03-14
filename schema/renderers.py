from rest_framework.renderers import JSONRenderer


class MyJsonRenderer(JSONRenderer):
    """
    Convention for repsonse data body
    The response data will alway follow this schema
    This render are used with `schema.pagination.MyBasePagination`
    for creating consistent api response that follow this schema
    {
        pageable?: {
            page: number:  number of page
            size: number:  size of current list
            next?: number:  next page number
            previous?: number:  previous page number
        },
        data: # actual data returned by a view
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Format for non-pageable api endpoint
        """
        status_code = renderer_context["response"].status_code
        formated_data = data

        if not (
            hasattr(data, "__iter__")
            and ("data" in data and "pageable" in data)
        ):
            formated_data = {"pageable": None, "data": data}

        formated_data["status_code"] = status_code
        return super().render(
            formated_data, accepted_media_type, renderer_context
        )
