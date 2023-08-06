"""解析jmx"""
from lxml import etree


class PropParser(object):
    def _parse_base_prop(self, node, type):
        data = {
            'name': node.get('name').split('.')[-1],
            'value': node.text,
            'type': type
        }
        return data

    def parse_element_prop(self, node):
        data = {'name': node.get('name').split('.')[-1],
                'value': [
                    self.parse_prop(node)
                    for node in node.getchildren()
                ]
                }
        return data

    def parse_collection_prop(self, node):
        name = node.get('name').split('.')[-1]
        data = {'name': name,
                'value': [self.parse_prop(node) or '' for node in node.getchildren()]
                }
        return data

    def parse_string_prop(self, node):
        return self._parse_base_prop(node, type='string')

    def parse_bool_prop(self, node):
        return self._parse_base_prop(node, type='boolean')

    def parse_int_prop(self, node):
        return self._parse_base_prop(node, type='integer')

    def parse_prop(self, node):
        prop_map = {
            'stringProp': self.parse_string_prop,
            'boolProp': self.parse_bool_prop,
            'intProp': self.parse_int_prop,
            'elementProp': self.parse_element_prop,
            'collectionProp': self.parse_collection_prop,
        }
        if node.tag not in prop_map:
            raise TypeError(f'不支持解析该属性: {node.tag}')
        parse_func = prop_map.get(node.tag)
        data = parse_func(node)
        return data

    def parse_props(self, parent):
        if parent.tag == 'hashTree':
            return []
        data = [self.parse_prop(node) for node in parent.getchildren()]
        return data


class JMXParser(object):
    def __init__(self, jmx_file):
        self.jmx_file = jmx_file
        xml = etree.parse(jmx_file)
        self.root = xml.getroot()

    def get_test_plan(self):
        test_plan = self.root.find('hashTree').find('TestPlan')
        return test_plan

    @staticmethod
    def get_children(node):
        following_hash_tree = node.getnext()
        if following_hash_tree is None:
            return []
        children = following_hash_tree.getchildren()
        return children

    @staticmethod
    def parse_attributes(node):
        data = dict(node.items())
        return data

    @staticmethod
    def parse_props(node):
        props = PropParser().parse_props(node)
        data = {prop['name']: prop['value'] for prop in props}
        return data

    def _parse_children(self, node):
        children = self.get_children(node)
        data = {child.tag: self._parse_node(child) for child in children}
        return data

    def _parse_node(self, node):
        attributes = self.parse_attributes(node)
        props = self.parse_props(node)
        if node.tag not in {'hashTree', 'stringProp', 'intProp', 'boolProp'}:
            children = self._parse_children(node)  # todo fix
        else:
            children = []
        # data = dict(**attributes, **props, **children)
        data = dict(attributes=attributes, props=props, children=children)
        return data

    def parse_dns_cache_manager(self, node):
        props = self.parse_props(node)
        hosts = [{'name': item['value'][0]['value'], 'address': item['value'][1]['value']}
                 for item in props.get('hosts', [])]
        return hosts

    def parse_cookie_manager(self, node):
        props = self.parse_props(node)
        data = {
            'clear_each_iteration': props.get('clearEachIteration') or ''
        }
        return data

    def parse_csv_file(self, node):
        attributes = self.parse_attributes(node)
        props = self.parse_props(node)
        data = {
            'name': attributes.get('testname'),
            'path': props.get('filename'),
            'varnames': props.get('variableNames'),
            'delimiter': props.get('delimiter'),
        }
        return data

    def parse_header_manager(self, node):
        props = self.parse_props(node)
        data = {item['value'][0]['value']: item['value'][1]['value'] for item in props.get('headers')}
        return data

    def parse_response_assertion(self, node):
        props = self.parse_props(node)
        data = {
            'test_field': props.get('test_field').split('.')[-1],
            'test_type': props.get('test_type'),
            'strings': [item['value'] for item in props.get('test_strings')],
        }
        return data

    def _parse_http_sampler_params(self, node):
        props = self.parse_props(node)
        content_type = 'data'
        if props.get('method') == 'GET':
            content_type = 'params'
        _params = {}
        for item in props.get('Arguments')[0]['value']:
            name = item['name']
            values = {sub_item['name']: sub_item['value'] for sub_item in item['value']}
            if name == '':
                content_type = 'raw_data'
                _params = values.get('value')
            else:
                _params[name] = values.get('value')
        return content_type, _params

    def _parse_sub_headers(self, node):
        header_managers = node.getnext().xpath('HeaderManager')
        _headers = [self.parse_header_manager(node) for node in header_managers]
        headers = {}
        [headers.update(item) for item in _headers]
        return headers

    def _parse_sub_csv_files(self, node):
        csv_data_sets = node.getnext().xpath('CSVDataSet')
        csv_files = [self.parse_csv_file(node) for node in csv_data_sets]
        return csv_files

    def _parse_sub_validate(self, node):
        response_assertions = node.getnext().xpath('ResponseAssertion')
        validate = [self.parse_response_assertion(node) for node in response_assertions]
        return validate

    def parse_http_sampler(self, node):
        attributes = self.parse_attributes(node)
        props = self.parse_props(node)
        content_type, _params = self._parse_http_sampler_params(node)
        headers = self._parse_sub_headers(node)

        csv_files = self._parse_sub_csv_files(node)
        validate = self._parse_sub_validate(node)

        request = {
            'protocol': props.get('protocol'),
            'domain': props.get('domain'),
            'port': props.get('port') or '',
            'encoding': props.get('contentEncoding') or '',
            'path': props.get('path'),
            'method': props.get('method'),
            'connect_timeout': props.get('connect_timeout') or '',
            'response_timeout': props.get('response_timeout') or '',
            'follow_redirects': props.get('contentEncoding') or '',
            'auto_redirects': props.get('auto_redirects'),
            'use_keepalive': props.get('use_keepalive'),
        }
        request[content_type] = _params
        request['headers'] = headers

        data = {
            'request_name': attributes.get('testname'),
            'enabled': attributes.get('enabled'),
            'comments': props.get('comments') or '',
            'csv_files': csv_files,
            'request': request,
            'validate': validate
        }
        return data

    def parse_dubbo_sample(self, node):
        attributes = self.parse_attributes(node)
        props = self.parse_props(node)
        registry = {
            'type': props.get('FIELD_DUBBO_REGISTRY_PROTOCOL') or '',
            'group': props.get('FIELD_DUBBO_REGISTRY_GROUP') or '',
            'address': props.get('FIELD_DUBBO_ADDRESS') or '',
        }
        dubbo = {'timeout': props.get('FIELD_DUBBO_TIMEOUT'), 'retires': props.get('FIELD_DUBBO_RETRIES'),
                 'group': props.get('FIELD_DUBBO_GROUP') or '', 'connections': props.get('FIELD_DUBBO_CONNECTIONS'),
                 'load_balance': props.get('FIELD_DUBBO_LOADBALANCE'), 'cluster': props.get('FIELD_DUBBO_CLUSTER'),
                 'service': props.get('FIELD_DUBBO_INTERFACE'), 'method': props.get('FIELD_DUBBO_METHOD'),
                 'headers': self._parse_sub_headers(node)}
        validate = self._parse_sub_validate(node)
        csv_files = self._parse_sub_csv_files(node)
        data = {
            'request_name': attributes.get('testname'),
            'enabled': attributes.get('enabled'),
            'comments': props.get('comments') or '',
            'csv_files': csv_files,
            'registry': registry,
            'dubbo': dubbo,
            'validate': validate

        }

        return data

    def parse_sub_http_samples(self, node):
        http_samples = node.getnext().xpath('HTTPSamplerProxy')
        data = [self.parse_http_sampler(node) for node in http_samples]
        return data

    def parse_sub_dubbo_samples(self, node):
        http_samples = node.getnext().xpath('io.github.ningyu.jmeter.plugin.dubbo.sample.DubboSample')
        data = [self.parse_dubbo_sample(node) for node in http_samples]
        return data

    def parse_thread_group(self, node):
        attributes = self.parse_attributes(node)
        props = self.parse_props(node)
        _controller = {item['name']: item['value'] for item in props.get('main_controller')}
        csv_files = self._parse_sub_csv_files(node)
        http_samples = self.parse_sub_http_samples(node)
        dubbo_samples = self.parse_sub_dubbo_samples(node)
        data = {'thread_group_name': attributes.get('testname'), 'enabled': attributes.get('enabled'),
                'comments': props.get('comments') or '', 'num_threads': props.get('num_threads'),
                'ramp_time': props.get('ramp_time'), 'scheduler': props.get('scheduler'),
                'duration': props.get('duration') or '', 'delay': props.get('delay') or '',
                'forever': _controller.get('continue_forever'), 'loops': _controller.get('loops'),
                'csv_files': csv_files, 'http_samples': http_samples, 'dubbo_samples': dubbo_samples}
        return data

    def parse_sub_thread_groups(self, node):
        thread_groups = node.getnext().xpath('ThreadGroup')
        data = [self.parse_thread_group(node) for node in thread_groups]
        return data

    def parse_sub_dns_cache_manager(self, node):
        dns_cache_managers = node.getnext().xpath('DNSCacheManager')
        data = []
        [data.extend(self.parse_dns_cache_manager(item)) for item in dns_cache_managers]
        return data

    def parse_sub_cookie_manager(self, node):
        cookie_managers = node.getnext().xpath('CookieManager')
        data = [self.parse_cookie_manager(node) for node in cookie_managers]
        if len(data) > 0:
            data = data[0]
        return data

    def parse_test_plan(self, ):
        node = self.get_test_plan()
        attributes = self.parse_attributes(node)
        props = self.parse_props(node)
        hosts = self.parse_sub_dns_cache_manager(node)
        cookies = self.parse_sub_cookie_manager(node)
        thread_groups = self.parse_sub_thread_groups(node)
        data = {
            'test_plan_name': attributes.get('testname'),
            'comments': props.get('props') or '',
            'hosts': hosts,
            'cookies': cookies,
            'thread_groups': thread_groups,
        }
        return data

    def to_dict(self):
        return self.parse_test_plan()

    @property
    def data(self):
        return self.to_dict()


class ModelBuilder(object):
    def __init__(self, request):
        self.creator = request.user
        self.operator = request.user
        print('创建人', self.creator, '操作人', self.operator)

    def create_test_plan(self, data, test_project_name) -> models.TestPlan:
        test_project = models.TestProject.objects.filter(name=test_project_name).first()
        test_plan = models.TestPlan.objects.create(
            test_project=test_project,
            name=data.get('test_plan_name'),
            desc=data.get('comments'),
            hosts=data.get('hosts'),
            clear_each_iteration=data.get('cookies', {}).get('clear_each_iteration') == 'true',
            creator=self.creator,
            operator=self.operator
        )
        for data in data.get('csv_files', []):
            data_file = self.create_data_file(data)
            test_plan.data_files.add(data_file)

        for data in data.get('thread_groups', []):
            self.create_thread_group(data, test_plan)

        return test_plan

    def create_data_file(self, data: dict) -> models.DataFile:
        data_file = models.DataFile.objects.create(
            name=data.get('name'),
            file=data.get('path'),
            var_names=data.get('varnames'),
            delimiter=data.get('delimiter'),
            creator=self.creator,
            operator=self.operator
        )
        return data_file

    def create_thread_group(self, data: dict, test_plan: models.TestPlan) -> models.ThreadGroup:
        thread_group = models.ThreadGroup.objects.create(
            test_plan=test_plan,
            name=data.get('thread_group_name'),
            desc=data.get('comments'),
            enabled=data.get('enabled') == 'true',
            num_threads=data.get('num_threads'),
            loops=data.get('loops'),
            ramp_time=data.get('ramp_time'),
            scheduler=data.get('scheduler') == 'true',
            duration=data.get('duration'),
            delay=data.get('delay') or 0
        )
        for csv_file in data.get('csv_files', []):
            data_file = self.create_data_file(csv_file)
            thread_group.data_files.add(data_file)

        for http_sample in data.get('http_samples', []):
            self.create_http_api_request(http_sample, thread_group)

        for dubbo_sample in data.get('dubbo_samples', []):
            self.create_http_api_request(dubbo_sample, thread_group)

        return thread_group

    def create_http_api_request(self, data: dict, thread_group: models.ThreadGroup) -> models.ApiRequest:
        data_request = data.get('request', {})
        api = self.get_or_create_api(
            protocol=data_request.get('protocol'),
            domain=data_request.get('domain'),
            url=data_request.get('path'),
            method=data_request.get('method'),
        )

        request = {
            'headers': data_request.get('headers', None),
            'params': data_request.get('params', None),
            'data': data_request.get('data', None),
            'raw_data': data_request.get('raw_data', None),
        }

        api_request = models.ApiRequest.objects.create(
            thread_group=thread_group,
            api=api,
            name=data.get('request_name'),
            desc=data.get('commens'),
            enabled=data.get('enabled') == 'true',
            connect_timeout=data_request.get('connect_timeout') or 0,
            response_timeout=data_request.get('response_timeout') or 0,
            follow_redirects=data_request.get('follow_redirects') == 'true',
            auto_redirects=data_request.get('auto_redirects') == 'true',
            use_keepalive=data_request.get('use_keepalive') == 'true',
            request=request,
            validate=data.get('validate')
        )

        return api_request

    def create_dubbo_api_request(self, data: dict, thread_group: models.ThreadGroup) -> models.ApiRequest:
        data_dubbo = data.get('dubbo', {})
        data_registry = data.get('registry', {})

        api = self.get_or_create_api(
            protocol='dubbo',
            domain=data_registry.get('address'),
            url=data_dubbo.get('service'),
            method=data_dubbo.get('method'),
        )

        request = {
            'headers': data_dubbo.get('headers', None),
            'params': data_dubbo.get('params', None),
        }

        api_request = models.ApiRequest.objects.create(
            thread_group=thread_group,
            api=api,
            name=data.get('request_name'),
            desc=data.get('commens'),
            enabled=data.get('enabled') == 'true',
            request=request,
            validate=data.get('validate')
        )

        return api_request

    def get_or_create_api(self, protocol, domain, url, method):
        project = Project.objects.first()  # todo
        api = Api.objects.filter(protocol=protocol, domain=domain,
                                 url=url, method=method).first()
        if not api:
            api = Api.objects.create(
                project=project,
                name=f'{protocol}://{domain}{url}',
                protocol=protocol,
                domain=domain,
                url=url,
                method=method,
                creator=self.creator,
                operator=self.operator
            )
        return api


if __name__ == '__main__':
    jmx = JMXParser("/apps/perftest/jmx/httpbin2.xml")
    data = jmx.to_dict()
    import jinja2
    from pprint import pprint

    TPL_FILE = 'tpl.xml'
    # 读取模板
    with open(TPL_FILE, encoding='utf-8') as f:
        tpl = f.read()

    jmx_file = 'demo5.jmx'

    # 生成jmx
    jmx = jinja2.Template(tpl).render(data)
    with open(jmx_file, 'w', encoding='utf-8') as f:
        f.write(jmx)

    pprint(data)
