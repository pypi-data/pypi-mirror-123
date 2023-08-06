from pathlib import Path

import CppHeaderParser
from jinja2 import Template


class Generator:
    def __init__(
            self,
            data_type_h_file_path,
            bind_consts_cpp_tpl_file_path,
            output_dir_path,
    ):
        self.data_type_h_file_path = data_type_h_file_path
        self.bind_consts_cpp_tpl_file_path = bind_consts_cpp_tpl_file_path
        self.output_dir_path = output_dir_path
        self.data_consts = []

    def parse_data_type(self):
        self.parse_data_type_enum()
        with self.data_type_h_file_path.open(encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith('#define'):
                    tokens = line.split()
                    if len(tokens) != 3:
                        continue
                    name = tokens[1]
                    value = tokens[2]
                    self.data_consts.append({
                        'name': name,
                        'value': value,
                    })

    def parse_data_type_enum(self):
        h = CppHeaderParser.CppHeader(self.data_type_h_file_path, encoding='utf-8')
        for enum in h.enums:
            for value in enum['values']:
                self.data_consts.append({
                    'name': value['name'],
                    'value': str(value['value']),
                })

    def render_template(self, tpl_file, output_file, data):
        tpl_content = tpl_file.read_text(encoding='utf-8')
        tpl = Template(tpl_content)
        r = tpl.render(**data)
        output_file.write_text(r, encoding='utf-8')

    def generate_consts(self):
        self.render_template(
            self.bind_consts_cpp_tpl_file_path,
            self.output_dir_path / 'bind_consts.cpp',
            {'data_consts': self.data_consts}
        )

    def generate(self):
        self.parse_data_type()
        self.generate_consts()


def main():
    current_dir = Path(__file__).parent
    data_type_h_file_path = current_dir / Path('../../libs/ctp/include/ThostFtdcUserApiDataType.h')
    bind_consts_cpp_tpl_file_path = current_dir / Path('templates/bind_consts.cpp.tpl')
    output_dir_path = current_dir / Path('../../src')

    generator = Generator(
        data_type_h_file_path,
        bind_consts_cpp_tpl_file_path,
        output_dir_path
    )
    generator.generate()


if __name__ == '__main__':
    main()
