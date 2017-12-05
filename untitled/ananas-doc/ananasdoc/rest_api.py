# -*- coding:utf-8 -*-
import os
import sys
import glob
import copy
import random
import string
import datetimeutil
import urllib
import exception as errors

from collections import OrderedDict

from utils import load_yaml_file, json_dump

reload(sys)
sys.setdefaultencoding("utf-8")


class AnanasRestApi(object):

    content = ""

    def __init__(self, **kwargs):
        """
        加载配置文件
        """
        self.config = kwargs.get('api_doc_config')
        self.path = kwargs.get('path')
        self.schema_template = self.config.get("schema_template") or "default"
        self.api_schema_mp = {
            "lcylln": self.process_resource_context_lcylln,
            "default": self.process_resource_context
        }
    def set_api(self):
        """

        :return:
        """
        self.content += "## " + self.config.get('title') + "\n\n"
        self.set_yml_md()
        self.make_md()

    def set_yml_md(self):
        """

        :return:
        """
        path = self.config.get('api_dir')
        leve_str = str(self.config.get('leve')) + "."
        leve = 1

        if self.schema_template != "lcylln":
            self.definitions = load_yaml_file(os.path.join(path, "definitions.yml"))
        else:
            self.definitions = {}

        try:
            for pkg_dir in glob.glob('%s/*' % path):
                if os.path.basename(pkg_dir) == "definitions.yml":
                    continue

                leve, leve_str = self.generate_content(pkg_dir, leve, leve_str)
        except errors.AnanasDocError, e:
            print "[Error]:" + str(e.code) + ":" + e.message
            exit()

    def generate_content(self, path, leve, leve_str):
        """
        :param path:
        :return:
        """
        if os.path.isdir(path):
            for p in os.listdir(path):
                return self.generate_content(os.path.join(path, p), leve, leve_str)
        else:
            if path.split(".")[-1] != "yml":
                raise Exception("the %s is not .yml format." % path)

            resource_text = load_yaml_file(path, False)
            for resource_def in resource_text:
                _leve_str = leve_str + str(leve)
                self.api_schema_mp[self.schema_template](resource_def, _leve_str)
                leve += 1

        return leve, leve_str

    def process_resource_context(self, resource_def, leve_str):
        """

        :param resource_def:
        :param leve_str:
        :return:
        """
        route_base = resource_def.get('route_base')
        description = resource_def.get('description')
        self.content += "\n### " + leve_str + "、" + description + "\n\n"
        leve = 1
        for route_patten, route_resp in resource_def['apis'].iteritems():
            api_name = route_patten
            uri = route_base + api_name
            for resp_method, resp_def in route_resp.iteritems():
                self.content += "#### " + leve_str + "." + str(leve) + "、" + resp_def.get('summary') + "\n\n"
                self.content += "**说明：**\n\n"
                self.content += str(resp_def.get('description')) + "\n\n"
                self.content += "**请求方式：**\n\n"
                self.content += "{0}\n\n".format(resp_method.upper())
                self.content += "**接口地址：**\n\n"
                self.content += "{0}\n\n".format(uri)
                self.content += "**请求参数：**\n\n"
                self.content += "|参数名称|类型|是否必须|枚举值|参数位置|描述|\n"
                self.content += "|:--------|:----|:--------|:------|:--------|:------|\n"
                # request params
                parameters = resp_def.get('parameters', None)
                if not parameters:
                    self.content += "|_|_|_|_|_|_|\n"
                self.set_req_md(copy.deepcopy(parameters))

                self.content += "\n"
                self.content += "**响应参数：**\n\n"
                self.content += "|参数名称|类型|描述|\n"
                self.content += "|:-------|:---|:----|\n"
                # response params
                responses = resp_def.get('responses', None)
                if not responses:
                    raise errors.ErrorSetApi('uri:%s, responses is error.', uri)
                self.set_resp_md(copy.deepcopy(responses))

                self.content += "\n\n"
                self.content += "**请求示例：**\n\n"
                self.content += "```\n"
                # request demo
                self.content += self.make_req_demo(copy.deepcopy(parameters), resp_method, uri)
                self.content += "\n"
                self.content += "```\n"
                self.content += "\n"
                self.content += "**响应示例：**\n\n"
                self.content += "```\n"
                # response demo
                self.content += self.make_resp_demo(copy.deepcopy(responses), uri)
                self.content += "\n"
                self.content += "```\n"
                self.content += "\n"
                leve += 1

    def process_resource_context_lcylln(self, resource_def, leve_str):
        """

        :param resource_def:
        :param leve_str:
        :return:
        """
        uri = resource_def["apis"]
        description = resource_def.get('description', "接口名")
        self.content += "\n### " + leve_str + "、" + description + "\n\n"
        leve = 1
        for method, params_mp in resource_def['method'].iteritems():
            self.content += "#### " + leve_str + "." + str(leve) + "、" + params_mp.get('summary', "接口功能描述") + "\n\n"
            if str(params_mp.get('description')):
                self.content += "**说明：%s**\n\n" % str(params_mp.get('description'))
            self.content += "**接口地址：%s**\n\n" % uri
            self.content += "**请求方式：%s**\n\n" % method.upper()
            self.content += "**请求参数：**\n\n"
            self.content += "|参数名称|类型|是否必须|允许值|参数位置|描述|\n"
            self.content += "|:--------|:----|:--------|:------|:--------|:------|\n"
            # request params
            parameters = params_mp.get('parameters', None)
            if not parameters:
                self.content += "|_|_|_|_|_|_|\n"
            self.set_req_md(copy.deepcopy(parameters))

            self.content += "\n"
            self.content += "**成功响应：**\n\n"
            self.content += "{\n\n}\n"

            leve += 1

    def set_req_md(self, rules):
        """

        :return:
        """
        if type(rules) == list:
            for rule in rules:
                self.set_req_params_md(rule)
                if rule['type'] == 'dict':
                    if rule.get('schema'):
                        self.set_req_md(rule)
        if type(rules) == dict:
            if rules['type'] == 'dict':
                for rule in rules['schema']:
                    rule['name'] = "{" + rules['name'] + "}." + rule.get('name', '')
                    self.set_req_params_md(rule)

    def set_req_params_md(self, rule):
        """

        :param content:
        :return:
        """
        required = rule.get('required', None)
        if required is True:
            rule['required'] = "是"
        elif required is False:
            rule['required'] = "否"
        else:
            rule['required'] = "未知"
        en_value_str = ""
        if rule.get('allowed', []):
            for en in rule['allowed']:
                en_value_str += str(en) + ","
        description = ""
        if rule.get('description', None):
            description = rule['description'].replace('|', '、')
        self.content += "|" + rule['name'] + \
                        "|" + rule['type'] + \
                        "|" + rule['required'] + \
                        "|" + en_value_str + \
                        "|" + rule['in'] + \
                        "|" + str(description) + \
                        "|\n"

    def set_resp_md(self, responses):
        """

        :return:
        """
        if responses.get("200"):
            ref = responses['200']['schema']['$ref']
        else:
            ref = responses['201']['schema']['$ref']
        schema = ref.split('/')[-1]
        responses_data = self.definitions[schema]
        if_set_response = True
        property_items = responses_data['properties'].items()
        property_keys = dict(property_items).keys()
        for key, value in property_items:
            if key == 'results' and value['type'] == 'list' and value.get('items') and '_meta' in property_keys:
                if_set_response = False
                self.content += "|_meta|dict|附加信息|\n"
                self.content += "|{_meta}.has_more|boolean|是否存在更多数据|\n"
                self.content += "|{_meta}.result_count|integer|数据总条数|\n"
                self.content += "|data|list|数据|\n"
                ref = value['items']['$ref']
                schema = ref.split('/')[-1]
                self.set_response(self.definitions[schema]['properties'], "[data].{i}")
            if key == 'extras':
                description = ""
                if value.get('description', None):
                    description = value['description'].replace('|', '、')
                self.content += "|" + key + "|" + value['type'] + "|" + description + "|\n"
        if if_set_response is True:
            self.set_response(responses_data['properties'])

    def set_response(self, data, type=''):
        if type:
            type += "."
        for key, value in data.items():
            if value.get('rename'):
                key = value['rename']
            description = ""
            if value.get('description', None):
                description = value['description'].replace('|', '、')
            self.content += "|" + type + key + "|" + value['type'] + "|" + description + "|\n"
            if (value['type'] in ["dict", "object_ref"]) and value.get('schema'):
                self.set_response(value['schema'], "{" + key + "}")
            if (value['type'] == "list") and value.get('items'):
                if value['items'].get('$ref'):
                    ref = value['items']['$ref']
                    schema = ref.split('/')[-1]
                    responses_data = self.definitions[schema]
                    self.set_response(responses_data['properties'], "[" + key + "].{i}")
                else:
                    self.set_response(value['items'], "[" + key + "].{i}")

    def make_req_demo(self, parameters, method, uri):
        """

        :return:
        """
        demo = self.make_req_data(parameters, {})
        if '{' in uri:
            path_params = {}
            for k in demo.keys():
                if k in uri:
                    path_params[k] = demo.pop(k, None)
            url = uri.format(**path_params)
        else:
            url = uri
        con = ""
        if method.upper() == "GET":
            con += urllib.urlencode(demo)
        if method.upper() == "POST":
            con += json_dump(demo)
        con += "\n"
        return con

    def make_req_data(self, rule, data):
        """

        :param rules:
        :return:
        """
        if isinstance(rule, dict):
            if rule.get('type') == "dict" and isinstance(rule.get('schema'), list):
                self.make_req_data(rule.get('schema'), data)
            else:
                data = self.filling_params(**rule)
            return data
        if isinstance(rule, list):
            for _rule in rule:
                data[_rule.get('name')] = self.make_req_data(_rule, {})
            return data

    def filling_params(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        param_name = kwargs.get('name', None)
        example = kwargs.get('example', None)
        if example:
            return example
        default = kwargs.get('default', None)
        if default:
            return default
        allow = kwargs.get('allow', None)
        if allow:
            return random.choice(allow)
        params_type = kwargs.get('type')
        if params_type in ['int', 'integer', 'number', 'long']:
            if param_name:
                if 'date' in param_name:
                    return 20170803
            return random.randint(1, 100)
        elif params_type in ['str', 'string', 'basestring', 'unicode', 'bytes']:
            if param_name:
                if 'mobile' in param_name:
                    return "18818881888"
                elif 'phone' in param_name:
                    return "18616661666"
                elif 'tel' in param_name:
                    return "010-88886666"
                elif 'address' in param_name:
                    return "北京市朝阳区通惠大厦"
                elif 'id' in param_name:
                    return random.choice(["5826650e3d65ce2d0665317f",
                                          "582661953d65ce2b7b5dde32",
                                          "5826650e3d65ce2d27645763",
                                          "580cb92e3d65ce09ebf7dc4e"])
                elif 'shipping_time' in param_name:
                    return "11:45"
                elif 'name' in param_name:
                    return random.choice(["驴与鱼", "绿与鱼", '绿与驴', '驴与绿', '小犟驴'])
                elif 'code' in param_name:
                    return ''.join(random.sample(string.digits, 6))
            return ''.join(random.sample(string.ascii_letters + string.digits, 6))
        elif params_type in ['bool', 'boolean']:
            return bool(random.getrandbits(1))
        elif params_type in ['date']:
            return int(datetimeutil.prc_now("%Y%m%d"))
        elif params_type in ['datetime']:
            return "2017-09-15T03:49:58.060000+00:00"
        elif params_type in ['float']:
            return random.uniform(30, 120)
        elif params_type in ['dict']:
            return {}
        elif params_type in ['list']:
            if param_name:
                if 'poi' in param_name:
                    return [116.23233, 39.12322]
            return []
        elif params_type in ['ObjectId', "objectid"]:
            return random.choice(["5826650e3d65ce2d0665317f",
                                  "582661953d65ce2b7b5dde32",
                                  "5826650e3d65ce2d27645763",
                                  "580cb92e3d65ce09ebf7dc4e"])
        return None

    def make_resp_demo(self, responses, uri):
        """

        :param responses:
        :param uri:
        :return:
        """
        if responses.get("200"):
            ref = responses['200']['schema']['$ref']
        else:
            ref = responses['201']['schema']['$ref']
        schema = ref.split('/')[-1]
        responses_data = self.definitions[schema]
        properties = responses_data.get('properties')
        if properties.get('_meta'):
            # object-set
            set_item_schema_ref = properties['results']['items']['$ref']
            result_ref = set_item_schema_ref.lstrip('#/definitions/')
            result = self.definitions.get(result_ref, None)
            if not result:
                print "[Error]:", result_ref, ' URL:', uri, ", not defind response schema."
                exit()
            else:
                result = self.make_resp_date(result.get('properties'), {})
                _result = {
                    "_meta": {
                        "has_more": True,
                        "result_count": random.randint(1, 10),
                    },
                    "data": [result]
                }
                return json_dump(_result)
        else:
            _result = self.make_resp_date(properties, {})
            return json_dump(_result)

    def make_resp_date(self, properties, data):
        if not isinstance(properties, dict):
            print "[Error]: response schema defind error."
            exit()
        for param_name, rule in properties.iteritems():
            if rule.get('rename'):
                param_name = rule.get('rename')
            if rule.get('type') and rule.get('type') in ["object_ref", 'dict'] and rule.get('schema'):
                data[param_name] = self.make_resp_date(rule.get('schema'), {})
            else:
                data[param_name] = self.filling_params(name=param_name, **rule)
        return data

    def make_md(self):
        """

        :return:
        """

        f = file(self.path + '/docs/api.md', "w+")
        f.write(self.content)
        f.close()




if __name__ == "__main__":
    kw = {
        "api_doc_config": {
            "if_set_api": True,
            "api_dir": "/Users/Song/Desktop/www/ananas-doc/api_schema",
            "leve": 2,
            "title": "接口文档",
            "schema_template": "lcylln"
        },
        'path': "/Users/Song/Desktop/www/ananas-doc",

    }
    a = AnanasRestApi(**kw)
    a.set_api()