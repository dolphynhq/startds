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

    def handle(self, name):
        self.validate_name(name)

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
