from __future__ import absolute_import
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from rest_framework.renderers import JSONRenderer
import shlex, subprocess
from rest_framework.parsers import JSONParser, MultiPartParser, DataAndFiles
import pdb
from django.utils.datastructures import MultiValueDict
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.contrib.auth.models import User
from django.conf import settings

class UtilClass:

    @staticmethod
    def inList(element, lista):
        for item in lista:
            if item == element:
                return True
        return False

    @staticmethod
    def objInList(element, lista):
        for item in lista:
            if item.id == element.id:
                return True
        return False

    @staticmethod
    def next_id(Instance, id):
        next = Instance.objects.filter(id__gt=id)
        if next.count() > 0:
            result = next.order_by("id").first().id
        else:
            result = None
        return result

    @staticmethod
    def previous_id(Instance, id):
        previous = Instance.objects.filter(id__lt=id)
        if previous.count() > 0:
            result = previous.order_by("-id").first().id
        else:
            result = None
        return result

    @staticmethod
    def dollar(num):
        n_decimales=2
        simbolo="$"
        n_decimales = abs(n_decimales)
        num = round(num, n_decimales)
        num, dec = str(num).split(".")
        dec += "0" * (n_decimales - len(dec))
        num = num[::-1]
        l = [num[pos:pos+3][::-1] for pos in range(0,50,3) if (num[pos:pos+3])]
        l.reverse()
        num = str.join(",", l)
        try:
            if num[0:2] == "-,":
                num = "-%s" % num[2:]
        except IndexError:
            pass
        if not n_decimales:
            return "%s %s" % (simbolo, num)
        return "%s %s.%s" % (simbolo, num, dec)

    @staticmethod
    def dict2obj(d):
        if isinstance(d, list):
            d = [UtilClass.dict2obj(x) for x in d]
        if not isinstance(d, dict):
            return d
        class C(object):
            pass
        o = C()
        for k in d:
            o.__dict__[k] = UtilClass.dict2obj(d[k])
        return o


class NestedMultipartParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super(NestedMultipartParser, self).parse(stream=stream, media_type=media_type, parser_context=parser_context)
        data = {}
        files = MultiValueDict()
        for key, value in result.data.items():
        	if '[' in key and ']' in key:
        		index_left_bracket = key.index('[')
        		index_right_bracket = key.index(']')
        		nested_dict_key = key[:index_left_bracket]
        		nested_value_key = key[index_left_bracket + 1:index_right_bracket]
        		if nested_dict_key not in data:
        			data[nested_dict_key] = {}
        		data[nested_dict_key][nested_value_key] = value
        	else:
        		data[key] = value
        for key, value in result.files.items():
        	if '[' in key and ']' in key:
        		index_left_bracket = key.index('[')
        		index_right_bracket = key.index(']')
        		nested_dict_key = key[:index_left_bracket]
        		nested_value_key = key[index_left_bracket + 1:index_right_bracket]
        		if nested_dict_key not in data:
        			data[nested_dict_key] = {}
        		data[nested_dict_key][nested_value_key] = value
        	else:
        		data[key] = value
        return data

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)