import os
import shutil
import stat
import startds
from startds.core.management.base import BaseCommand

class TemplateCommand(BaseCommand):

    rewrite_template_suffixes = (
        ('.py-tpl', '.py'),
        ('.sh-tpl', '.sh'),
        ('Dockerfile-tpl', 'Dockerfile'),
        ('.gitignore-tpl', '.gitignore'),
        ('.gitkeep-tpl', '.gitkeep'),
        ('.dockerignore-tpl', '.dockerignore'),
        ('.txt-tpl', '.txt'),
        ('.md-tpl', '.md'),
        ('.env-tpl', '.env'),
        ('.yaml-tpl', '.yaml'),
    )

    def handle(self, name, options):
        self.validate_name(name)
        try:
            result = self.handle_options(options)
        except Exception as e:
            print(e)
            raise e
            
        
        top_dir = os.path.join(os.getcwd(), name)
        try:
            os.makedirs(top_dir)
        except FileExistsError:
            print(f'{top_dir} already exists')
            raise Exception(f'{top_dir} already exists')
        except OSError as e:
            print(e)
            raise Exception(e)
        
        base_name = 'exp_name'
        template_dir = os.path.join(list(startds.__path__)[0], 'conf', 'exp_template')
        prefix_length = len(template_dir) + 1

        for root, dirs, files in os.walk(template_dir):
            folder_name = root.split('/')[-1]
            folder_parent_name = root.split('/')[-2]
            folder_gp_name = root.split('/')[-3]

            if result.get('mode', '') == 'eng' and ( folder_name in ['explore', 'clean', 'transform', 'train'] 
            or folder_parent_name in ['explore', 'clean', 'transform', 'train']
            or folder_gp_name in ['explore', 'clean', 'transform', 'train']):
                continue
            elif result.get('mode', '') == 'ds' and ( folder_name in ['_apis', '_tests', '_orchestrate', '_apps']
            or folder_parent_name in ['_apis', '_tests', '_orchestrate', '_apps']
            or folder_gp_name in ['_apis', '_tests', '_orchestrate', '_apps']):
                continue
            else:
                pass

            if result.get('api', '') == 'flask' and folder_name in ['fastapi', 'cortex', 'bentoml']:
                continue
            elif result.get('api', '') == 'fastapi' and folder_name in ['flask', 'cortex', 'bentoml']:
                continue
            elif result.get('api', '') == 'cortex' and folder_name in ['flask', 'fastapi', 'bentoml']:
                continue
            elif result.get('api', '') == 'bentoml' and folder_name in ['flask', 'fastapi', 'cortex']:
                continue
            else:
                pass
            
            rel_path_to_root = root[prefix_length:]
            relative_dir = rel_path_to_root.replace(base_name, name)
            if relative_dir:
                target_dir = os.path.join(top_dir, relative_dir)
                os.makedirs(target_dir, exist_ok=True)

            for filename in files:
                old_path = os.path.join(root, filename)

                new_path = os.path.join(
                    top_dir, relative_dir, filename.replace(base_name, name)
                )
                for old_suffix, new_suffix in self.rewrite_template_suffixes:
                    if new_path.endswith(old_suffix):
                        new_path = new_path[:-len(old_suffix)] + new_suffix
                        break  # Only rewrite once

                if os.path.exists(new_path):
                    raise Exception(
                        f'{new_path} already exists. Overlaying experiment into an existing '
                        'directory won\'t replace conflicting files.'
                    )

                shutil.copyfile(old_path, new_path)
                try:
                    shutil.copymode(old_path, new_path)
                    self.make_writeable(new_path)
                except Exception:
                    pass
        
    def validate_name(self, name):
        if name is None:
            raise Exception('You must provide an experiment name.')

        if not name.isidentifier():
            raise Exception(f'{name} is not a valid experiment name.')


    def make_writeable(self, filename):
        if not os.access(filename, os.W_OK):
            st = os.stat(filename)
            new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
            os.chmod(filename, new_permissions)

    def handle_options(self, options):
        result = {'api': '', 'mode':''}
        if 'api' in options:
            api_val = options['api']
            if api_val is None:
                api_val = 'all'
            else:
                api_val = api_val[0]
            
            api_val = api_val.lower()
            if api_val not in ['fastapi', 'flask', 'cortex', 'bentoml', 'all']:
                raise Exception('Incorrect api value provided')
            else:
                result['api'] = api_val
        
        if 'mode' in options:
            mode_val = options['mode']
            if mode_val is None:
                mode_val = 'all'
            else:
                mode_val = mode_val[0]
            
            mode_val = mode_val.lower()
            if mode_val not in ['eng', 'ds', 'all']:
                raise Exception('Incorrect mode value provided')
            else:
                result['mode'] = mode_val
        
        return result
