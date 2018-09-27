from django.utils.six.moves.urllib import parse as urlparse
from rest_framework.schemas import AutoSchema
import yaml
import coreapi
from rest_framework_swagger.views import get_swagger_view


class CustomSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        """Custom the coreapi using the func.__doc__ .

        if __doc__ of the function exsit, use the __doc__ building the coreapi. else use the default serializer.

        __doc__ in yaml format, eg:

        desc: the desc of this api.
        ret: when success invoked, return xxxx
        err: when error occured, return xxxx
        input:
        - name: mobile
          desc: the mobile number
          type: string
          required: true
          location: form
        - name: promotion
          desc: the activity id
          type: int
          required: true
          location: form
        """
        view = self.view
        method_name = getattr(view, 'action', method.lower())
        _method_desc = ''

        fields = self.get_path_fields(path, method)

        func = getattr(view, view.action) if getattr(view, 'action', None) else None
        if func and func.__doc__:
            try:
                yaml_doc = yaml.load(func.__doc__)
            except:
                yaml_doc = None

            # Extract schema information from yaml

            if yaml_doc and type(yaml_doc) != str:
                _desc = yaml_doc.get('desc', '')
                _ret = yaml_doc.get('ret', '')
                _err = yaml_doc.get('err', '')
                _method_desc = _desc + '\n<br/>' + 'return: ' + _ret + '<br/>' + 'error: ' + _err
                params = yaml_doc.get('input', [])

                for i in params:
                    _name = i.get('name')
                    _desc = i.get('desc')
                    _required = i.get('required', False)
                    _type = i.get('type', 'string')
                    _location = i.get('location', 'form')
                    field = coreapi.Field(
                        name=_name,
                        location=_location,
                        required=_required,
                        description=_desc,
                        type=_type
                    )
                    fields.append(field)
            else:
                _method_desc = func.__doc__ if func and func.__doc__ else ''
                fields += self.get_serializer_fields(path, method, view)

        fields += self.get_pagination_fields(path, method)
        fields += self.get_filter_fields(path, method)

        manual_fields = self.get_manual_fields(path, method)
        fields = self.update_fields(fields, manual_fields)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method)
        else:
            encoding = None

        if base_url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urlparse.urljoin(base_url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=_method_desc
        )