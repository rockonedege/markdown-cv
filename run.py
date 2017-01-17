import os
from os import path
from datetime import date

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def this_folder():
    import os
    return os.path.dirname(os.path.abspath(__file__))

def par_folder():
    return path.join(this_folder(), '..')

def make_if_none(directory):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

#
# paths of sources
#
gnerator_root =  path.join(this_folder(), 'generator')
themes_root = path.join(gnerator_root, 'bootswatch-themes', '4')
md_root = path.join(gnerator_root, '..', 'markdown')
pics_root = path.join(md_root, 'pics')
js_root = path.join(gnerator_root, 'js')
css_root = path.join(gnerator_root, 'css')
html_root = path.join(gnerator_root, 'html')

#
# path of output, make sure it exists
#
out_root = path.join(this_folder(), 'output')
make_if_none(out_root)


def mds():
    return [md.rpartition('.')[0] for md in os.listdir(md_root) if md.lower().endswith('.md')]

def srcify_imgs():
    
    def b64fy():

        import base64

        final = {}
        imgs = [img for img in os.listdir(pics_root) if img.lower().endswith('jpg') or img.lower().endswith('png')]
        for img in imgs:
            with open(path.join(pics_root, img), "rb") as f:            
                final[img] = base64.b64encode(f.read()).decode('utf-8')
        return final

    t = '<img width="1080" src="data:image/{format};base64,{data}" alt="{name}">'
    return {k : t.format(format = k.rpartition('.')[-1],  data = v,  name = k) for k, v in b64fy().items()} 


def run(name, theme):
    """ Generate bootswatch base html files.
    - http://bootswatch.com/
    inspiried by
    - https://github.com/arturadib/strapdown
    - http://strapdownjs.com/
    """
    
    import re 
    r = re.compile(r'!\[.*\]\((.+)\)', re.I) # ![]()


    def insert_img(lines):

        imgs = srcify_imgs()

        def per_(line):

            def repl(mo):
                link = mo.group(1)
                name = link.split('\\')
                name = name[-1] if len(name) != 1 else link.split('/')[-1]
                try:
                    line = imgs[name]
                    logging.info('replaced %s' % link)
                    # logging.info('replaced %s with %s' % (link, line))
                except KeyError as e:
                    logging.info('skip %s' % name)

                return line

            return re.sub(r, repl, line)

        return [per_(line) for line in lines]



    def is_cv():
        return name.lower().startswith('cv')

    # markdown input
    def input(name):

        where = path.join(md_root, name + '.md')

        def handle_cv(lines):
            title = 'Resume &middot; Tom Tan &middot; Last updated at {date}' if 'en' in name else '简历 &middot; 谭智 &middot; 最后更新于 {date}'

            title = title.format(date = date.today())
            return title, ''.join(lines)

        def handle_projects(lines):

            if os.path.exists(pics_root):
                lines = insert_img(lines)
            for line in lines:
                if line.startswith('# '):
                    brand = line.partition(' ')[-1]
                    break

            title = '{brand} &middot; Tom Tan &middot; Last updated at {date}'

            title = title.format(
                brand = ' '.join(name.split('-')[:-1]).upper(),
                date = date.today())

            lines = [ line # + '\n' if line.lstrip().startswith('* ') else line
                        for line in lines if not line.startswith('# ')]
            lines.extend(['-----\n', '<small>Last updated at{}.</small>'.format(date.today())])
            return title, '\n'.join(lines)          

        with open(where, encoding='utf-8') as f:
            lines = f.readlines()

            if is_cv():                
                return handle_cv(lines)
            else:              
                return handle_projects(lines)
                        
    def css(theme):

        css = []
        for p in [
                path.join(themes_root, theme + '.min.css'),
                path.join(css_root, 'markcv.css')
            ]:
            with open(p) as f:
                css.append('<style>{css}</style>'.format(css = f.read()))

        return '\n'.join(css)

    def js():

        js = []
        for p in [
                path.join(js_root, 'marked.min.js'),
                path.join(js_root, 'prettify.min.js'),
                path.join(js_root, 'bootstrap.min.js'),
                path.join(js_root, 'markcv.js')
            ]:
            with open(p, encoding='utf-8') as f:
                js.append('<script>{js}</script>'.format(js = f.read()))

        return '\n'.join(js)

    def html(title, markdown, theme, flavor):

        template = 'cv-template.html' if is_cv() else 'projects-template.html'

        with open(path.join(html_root, template)) as f:
            t = f.read()

        return t.format(
                title=title,
                theme=theme,
                flavor=flavor, 
                markdown=markdown, 
                css=css(theme),
                js=js()
        )


    # html output
    def output(name, theme):

        out_folder = path.join(out_root, theme)
        make_if_none(out_folder)
        
        for flavor in [
                        'primary', 
                        'faded',
                        'inverse'
                        ]:

            out_file =  path.join(out_folder, '.'.join([name, theme, flavor, 'html']))


            title, markdown = input(name)

            with open(out_file, 'w+', encoding='utf-8') as f:
                    f.write(html(title, markdown, theme, flavor))
                    logging.info('done generating {file}'.format(file=out_file))

    output(name, theme)



def go():

    # [
    # 'cerulean', 'cosmo', 'custom', 'cyborg', 'darkly', 'flatly', 'journal', 'litera', 
    # 'lumen', 'lux', 'materia', 'minty', 'pulse', 'sandstone', 'simplex', 'slate', 
    # 'spacelab', 'superhero', 'united', 'yeti'
    # ]

    themes =[theme.partition('.')[0] 
                for theme in os.listdir(themes_root) 
                if theme.endswith('css')]
        
    for theme in themes:
      
        logging.info('generating theme {}'.format(theme))
        for md in mds():
            run(md, theme)

    logging.info('{} themes in `total.'.format(len(themes)))

go()