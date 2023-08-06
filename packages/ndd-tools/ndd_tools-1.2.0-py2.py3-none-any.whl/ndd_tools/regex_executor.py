import os
import yaml
import re
import json
from typing import List, Dict, Optional, Union
from pydantic import BaseModel
from .validators import check_instance_of
from .schemas import EnumStrategy, EnumGroupType
from .schemas import RegexExecutorConfig, ObjectRegexConfig
from .schemas import ObjFieldRegexConfig, ObjFieldPatternRegexConfig


def load_regex_config_file(file_path: str):
    if not isinstance(file_path, str) or not os.path.isfile(file_path):
        raise ValueError(f'file path wrong format, must be string path')
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        return RegexExecutorConfig.parse_obj(data)


class RegexResult:

    def __init__(self, result: dict[str, list[dict[str, Union[list, object]]]]) -> None:
        if not isinstance(result, dict):
            raise ValueError(f'result must be a dict')
        # example:
        # result = {
        #   'key': {
        #       'result': [],
        #       'source': {<object>}
        #   }
        # }
        self.result = result

    def _validate_key(self, key):
        if key not in self.result:
            raise ValueError(f'key {key} is not exist')

    def get(self, key: str, index: int = 0):
        self._validate_key(key)

        # index < 0 -> get all
        if index < 0:
            return self.result.get(key)[0].get('result')

        result = self.result.get(key)[0].get('result')
        if result:
            if isinstance(result, list):
                return result[index]
            if isinstance(result, str):
                print(result)
                return None
            

    def detail(self, key: str):
        self._validate_key(key)
        return self.result.get(key)

    def dict(self, detail=False):
        if detail:
            return self.result
        else:
            return {k: self.get(k) for k in self.result.keys()}

    def json(self, detail=False):
        if detail:
            return json.dumps(self.result)
        else:
            return json.dumps(self.dict(detail))


class RegexExecutor:
    def __init__(
        self,
        config_file_path: str = None,
        config: RegexExecutorConfig = None
    ) -> None:
        check_instance_of(config_file_path, str, True)
        check_instance_of(config, RegexExecutorConfig, True)
        self.config_file_path: str = config_file_path
        self.config: RegexExecutorConfig = config

    def set_config_file_path(self, config_file_path: str):
        check_instance_of(config_file_path, str)
        self.config_file_path = config_file_path
        self._load_config_from_file_path()

    def set_config(self, config: RegexExecutorConfig):
        check_instance_of(config, RegexExecutorConfig)
        self.config = config

    def _load_config_from_file_path(self, file_path: str = None):
        if not file_path:
            file_path = self.config_file_path
        return load_regex_config_file(file_path)

    def _get_data_of_path(self, current_path: List[str], input_data: Dict):
        if isinstance(input_data, list) and len(current_path) == 0:
            return input_data
        result = input_data
        for i in current_path:
            result = result[i]
        return result

    def build_field_paths(self, access_paths: List[str], input_data: Dict):
        result_paths = []
        for item in access_paths:
            if len(result_paths) == 0:
                if item == '[...]':
                    data_of_path = self._get_data_of_path([], input_data)
                    for i in range(len(data_of_path)):
                        result_paths.append([i])
                else:
                    result_paths.append([item])
            else:
                if item == '[...]':
                    # print('current result paths ', result_paths)
                    deleted_rpaths = []
                    new_paths = []
                    for rpath in result_paths:
                        data_of_path = self._get_data_of_path(rpath, input_data)
                        # print('check path', rpath, data_of_path)
                        for i in range(len(data_of_path)):
                            new_path = rpath + [i]
                            new_paths.append(new_path)
                            # print('\t\tnew path', new_path)
                        deleted_rpaths.append(rpath)
                    for np in new_paths:
                        result_paths.append(np)
                    for dp in deleted_rpaths:
                        result_paths.remove(dp)
                else:
                    for rpath in result_paths:
                        rpath.append(item)
        return result_paths

    def find_field_values(self, access_path: List[str], input_data: Dict) -> List[str]:
        paths = self.build_field_paths(access_path, input_data)
        final_result = []
        for path in paths:
            temp_result = input_data
            for item in path:
                temp_result = temp_result[item]
            final_result.append(temp_result)
        return final_result

    def handle_strategy(self, source: str, field_conf: ObjFieldRegexConfig):
        # print('handle source ', source, ' with ', field_conf)
        # return "OK, i hope so"
        if field_conf.strategy == EnumStrategy.GETALL:
            return {'result': source, 'source': source}

        if field_conf.strategy == EnumStrategy.MATCH:
            return {'result': self._execute_match(source, field_conf.patterns), 'source': source}

        if field_conf.strategy == EnumStrategy.SEARCH:
            return {'result': self._execute_search(source, field_conf.patterns), 'source': source}

        if field_conf.strategy == EnumStrategy.FINDALL:
            return {'result': self._execute_findall(source, field_conf.patterns), 'source': source}

        if field_conf.strategy == EnumStrategy.FINDITER:
            return {'result': self._execute_finditer(source, field_conf.patterns), 'source': source}

        raise ValueError('strategy must provide')

    def process_data(self, data: Dict, config: ObjectRegexConfig):
        check_instance_of(data, dict)
        check_instance_of(config, ObjectRegexConfig)
        result = {}
        for field in config.regex_fields:
            source_strings = self.find_field_values(field.field, data)
            # print('source', source_strings)
            result[field.key] = [self.handle_strategy(source, field) for source in source_strings]
        return result

    def _validate_before_execute(self, data: str, patterns: List[ObjFieldPatternRegexConfig]):
        check_instance_of(data, str)
        check_instance_of(patterns, list)
        for item in patterns:
            check_instance_of(item, ObjFieldPatternRegexConfig)

    def _execute_match(self, data: str, patterns: List[ObjFieldPatternRegexConfig]):
        self._validate_before_execute(data, patterns)
        for pattern in patterns:
            try:
                result = re.match(r'%s' % pattern.value, data, flags=re.I)
                if pattern.group_type == EnumGroupType.GROUPDICT:
                    return [i.groupdict() for i in result]
                if pattern.group_type == EnumGroupType.GROUP:
                    return "finditer not support group yet"
                if pattern.group_type == EnumGroupType.GROUPS:
                    return "finditer not support groups yet"

            except Exception as e:
                pass

    def _execute_search(self, data: str, patterns: List[ObjFieldPatternRegexConfig]):
        self._validate_before_execute(data, patterns)
        # print('_execute_search', data)
        for pattern in patterns:
            # print('_execute_search', pattern)
            try:
                result = re.search(r'%s' % pattern.value, data, flags=re.I)
                # print('_execute_search result', result)
                if pattern.group_type == EnumGroupType.GROUPDICT:
                    return [i.groupdict() for i in result]
                if pattern.group_type == EnumGroupType.GROUP:
                    _r = []
                    for index in pattern.group_indexes:
                        _r.append(result.group(index))
                    if not _r:
                        continue
                    return _r
                if pattern.group_type == EnumGroupType.GROUPS:
                    return result.groups()
            except IndexError as e:
                raise e
            except Exception as e:
                # print('get exception ', e)
                pass

    def _execute_findall(self, data: str, patterns: List[ObjFieldPatternRegexConfig]):
        self._validate_before_execute(data, patterns)
        # print('_execute_findall', data)
        for pattern in patterns:
            try:
                # print('_execute_findall pattern ', pattern)
                return re.findall(r'%s' % pattern.value, data, flags=re.I)
            except IndexError as e:
                raise e
            except Exception as e:
                pass

    def _execute_finditer(self, data: str, patterns: List[ObjFieldPatternRegexConfig]):
        self._validate_before_execute(data, patterns)
        for pattern in patterns:
            try:
                result = re.finditer(r'%s' % pattern.value, data, flags=re.I)
                if pattern.group_type == EnumGroupType.GROUPDICT:
                    return [i.groupdict() for i in result]
                if pattern.group_type == EnumGroupType.GROUP:
                    return "finditer not support group yet"
                if pattern.group_type == EnumGroupType.GROUPS:
                    return "finditer not support groups yet"
            except IndexError as e:
                raise e
            except Exception as e:
                pass

    def run(self, input_data: dict, config_name: str):
        check_instance_of(input_data, dict)
        check_instance_of(config_name, str)
        config: ObjectRegexConfig = self.config.config.get(config_name)
        return RegexResult(self.process_data(input_data, config))
