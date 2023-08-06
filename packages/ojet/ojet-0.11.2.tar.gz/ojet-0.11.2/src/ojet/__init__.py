def genelem(name, etype=2, hyphen='é', defclass=lambda x: '',mparameters=[]):
    def constructor(self, *elements, **attributes):
        self.elements = list(elements)
        self.mparameters = mparameters
        self.attributes = dict()
        self.containers = dict()
        self.defclasses = dict()
        idefclass = attributes['defclass'] if 'defclass' in attributes else defclass
        if etype==3:
            for p in self.mparameters: 
                if p not in attributes: raise Exception(f'{p} is a mandatory attribute for class: {name.__name__}!')
            self.id=attributes['id']
            ko = attributes['jsparameters']['knockout']
            self.containers[self.id] = lambda  c: f'\n{ko}.applyBindings(new {c}_OjetClass(), document.getElementById("{c}_container"));'
            self.defclasses[self.id] = lambda c: f'''
                class {c}_OjetClass {{
                    constructor() {{
                    {idefclass(attributes['jsparameters']) if 'jsparameters' in attributes else ''}
                    }}
                }}
            '''
        for a in attributes.keys():
            if a[0] == '_': self.attributes[a[1:]] = attributes[a].replace(hyphen, '-')
        if 'father' in attributes.keys() and attributes['father']: attributes['father'].elements.append(self)
    def render(self):
        ret =[]
        for a in self.attributes: 
            if '"' in self.attributes[a]: ret.append(f" {a}='{self.attributes[a]}'")
            else: ret.append(f' {a}="{self.attributes[a]}"')
        attribs = ''.join(ret)
        if etype == 1: return f'<{name.__name__}{attribs}/>'
        else:
            ret = []
            for e in self.elements:
                try: ret.append(e.render())
                except: ret.append(e)
                if hasattr(e, 'containers'): self.containers.update(e.containers)
                if hasattr(e, 'defclasses'): self.defclasses.update(e.defclasses)
            elems = ''.join(ret)
            return f'<{name.__name__}{attribs}>{elems}</{name.__name__}>'
    def add(self, element):
        self.elements.append(element)
    name = type(name, (object,), dict(__init__= constructor, render=render,add=add))
    return name

def classtofunc(x):
    f = lambda *elements, **attributes: x(*elements, **attributes)
    return f

LINK = classtofunc(genelem('link', 1))
META = classtofunc(genelem('meta', 1))

BODY = classtofunc(genelem('body', 2))
DIV = classtofunc(genelem('div', 2))
HEAD = classtofunc(genelem('head', 2))
HTML = classtofunc(genelem('html', 2))
H1 = classtofunc(genelem('h1', 2))
H2 = classtofunc(genelem('h2', 2))
H3 = classtofunc(genelem('h3', 2))
H4 = classtofunc(genelem('h4', 2))
H5 = classtofunc(genelem('h5', 2))
H6 = classtofunc(genelem('h6', 2))
OJBINDFOREACH = classtofunc(genelem('oj-bind-for-each', 2))
OJBINDTEXT = classtofunc(genelem('oj-bind-text', 2))
OJBUTTONSETMANY = classtofunc(genelem('oj-buttonset-many', 2))
OJCHARTITEM = classtofunc(genelem('oj-chart-item', 2))
OJCHARTSERIES = classtofunc(genelem('oj-chart-series', 2))
OJMENU = classtofunc(genelem('oj-menu', 2))
OJMENUBUTTON = classtofunc(genelem('oj-menu-button', 2))
OJOPTION = classtofunc(genelem('oj-option', 2))
OJTREEMAPNODE = classtofunc(genelem('oj-treemap-node', 2))
P = classtofunc(genelem('p', 2))
SCRIPT = classtofunc(genelem('script', 2))
SPAN = classtofunc(genelem('span', 2))
STYLE = classtofunc(genelem('style', 2))
TABLE = classtofunc(genelem('table', 2))
TD = classtofunc(genelem('td', 2))
TEMPLATE = classtofunc(genelem('template', 2))
TITLE = classtofunc(genelem('title', 2))
TR = classtofunc(genelem('tr', 2))

OJBUTTON = lambda *elements,**attributes: SPAN(genelem('oj-button', 3, mparameters=['id'])(*elements, **attributes), _id=f'{attributes["id"]}_container')
OJLABEL = lambda *elements,**attributes: SPAN(genelem('oj-label', 3, mparameters=['id'])(*elements, **attributes), _id=f'{attributes["id"]}_container')
OJLEDGAUGE = lambda *elements,**attributes: SPAN(genelem('oj-led-gauge', 3, mparameters=['id'])(*elements, **attributes), _id=f'{attributes["id"]}_container')

Ojchartconstructor = lambda jsparameters: f'''
                            this.dataProvider=new {jsparameters['ojs/ojarraydataprovider']}({jsparameters['data']},{{keyAttributes: "id"}});
                            this.hiddenCategories = {jsparameters['knockout']}.observableArray([]);
                            this.categoryInfo = {jsparameters['knockout']}.pureComputed(() => {{
                                const categories = this.hiddenCategories();
                                return categories.length > 0 ? categories.join(", ") : "none";
                            }});
'''
OJCHART = lambda *elements,**attributes: SPAN(attributes['title'], genelem('oj-chart', 3, mparameters=['id', 'jsparameters', 'title'], defclass=Ojchartconstructor)(*elements, _data='[[dataProvider]]', **attributes), _id=f'{attributes["id"]}_container')
OJTOOLBAR = lambda *elements,**attributes: SPAN(genelem('oj-toolbar', 3, mparameters=['id'])(*elements, **attributes), _id=f'{attributes["id"]}_container')
OJTREEMAP = lambda *elements,**attributes: SPAN(genelem('oj-treemap', 3, mparameters=['id', 'jsparameters'])(*elements, **attributes), _id=f'{attributes["id"]}_container')
OJTREEVIEW = lambda *elements,**attributes: SPAN(genelem('oj-tree-view', 3, mparameters=['id', 'jsparameters'])(*elements, **attributes), _id=f'{attributes["id"]}_container')

def GENSTYLE(name, value, anchor=None):
    anchor.styles[name] = value
    STYLE(f'.{name} {value}', father=anchor.head)
    
BASICTEMPLATE = TEMPLATE(OJCHARTITEM(**{"_value": "[[item.data.value]]","_group-id": "[[ [item.data.category] ]]","_series-id": "[[item.data.serie]]", "_hidden_categories": "{{hiddenCategories}}"}), **{"_slot": "itemTemplate", "_data-oj-as": "item"})         
BOXTEMPLATE = TEMPLATE(OJCHARTITEM(**{"_items": "[[item.data.outliers]]", "_q1": "[[item.data.q1]]", "_q2": "[[item.data.q2]]", "_q3": "[[item.data.q3]]", "_high": "[[item.data.high]]", "_low": "[[item.data.low]]","_group-id": "[[ [item.data.group] ]]","_series-id": "[[item.data.series]]", "_hidden_categories": "{{hiddenCategories}}"}), **{"_slot": "itemTemplate", "_data-oj-as": "item"})         
BUBBLETEMPLATE = TEMPLATE(OJCHARTITEM(**{"_x": "[[item.data.x]]", "_y": "[[item.data.y]]", "_z": "[[item.data.z]]", "_group-id": "[[ [item.data.group] ]]","_series-id": "[[item.data.series]]", "_hidden_categories": "{{hiddenCategories}}"}), **{"_slot": "itemTemplate", "_data-oj-as": "item"})         
RANGETEMPLATE = TEMPLATE(OJCHARTITEM(**{"_high": "[[item.data.high]]", "_low": "[[item.data.low]]","_group-id": "[[ [item.data.group] ]]","_series-id": "[[item.data.series]]", "_hidden_categories": "{{hiddenCategories}}"}), **{"_slot": "itemTemplate", "_data-oj-as": "item"})         
SCATTERTEMPLATE = TEMPLATE(OJCHARTITEM(**{"_x": "[[item.data.x]]", "_y": "[[item.data.y]]", "_group-id": "[[ [item.data.group] ]]","_series-id": "[[item.data.series]]", "_hidden_categories": "{{hiddenCategories}}"}), **{"_slot": "itemTemplate", "_data-oj-as": "item"})         

class Ojet:

    def __init__(self, title=None):
        STYLEIMPORT = '''
            @import url('https://static.oracle.com/cdn/jet/11.1.0/default/css/redwood/oj-redwood-min.css');
            @import url('https://static.oracle.com/cdn/fnd/gallery/2107.3.0/images/iconfont/ojuxIconFont.min.css');
        '''
        LIBSANDLANG = '''
              var browserLang = window.navigator.language || window.navigator.userLanguage;
              requirejs.config({
                paths: {
                    'knockout': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/knockout/knockout-3.5.1',
                    'jquery': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/jquery/jquery-3.6.0.min',
                    'jqueryui-amd': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/jquery/jqueryui-amd-1.12.1.min',
                    'hammerjs': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/hammer/hammer-2.0.8.min',
                    'ojdnd': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/dnd-polyfill/dnd-polyfill-1.0.2.min',
                    'ojs': 'https://static.oracle.com/cdn/jet/11.1.0/default/js/min',
                    'ojL10n': 'https://static.oracle.com/cdn/jet/11.1.0/default/js/ojL10n',
                    'ojtranslations': 'https://static.oracle.com/cdn/jet/11.1.0/default/js/resources',
                    'preact': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/preact/dist/preact.umd',
                    'text': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/require/text',
                    'signals': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/js-signals/signals.min',
                    'touchr': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/touchr/touchr',
                    'customElements': 'https://static.oracle.com/cdn/jet/v8.3.0/3rdparty/webcomponents/custom-elements.min',
                    'css': 'https://static.oracle.com/cdn/jet/11.1.0/3rdparty/require-css/css.min'
                },
                config: {
                  i18n: { locale: browserLang },
                  ojL10n: { locale: browserLang }
                }
              });
      '''
        
        self.styles = dict()
        self.functions = dict()
        self.html = HTML()
        self.head = HEAD(father = self.html)
        self.meta1 = META(father=self.head, _charset='utf-8')
        self.meta2 = META(father=self.head, _keywords='cpu')
        self.meta3 = META(father=self.head, _name='description', _content='Charts showing cpu data from exawatcher')
        self.styleimport = STYLE(STYLEIMPORT, father=self.head, _type='text/css')
        self.script1 = SCRIPT(father=self.head, _src="https://static.oracle.com/cdn/jet/11.1.0/3rdparty/require/require.js")
        self.script2 = SCRIPT(LIBSANDLANG, father=self.head, _type='text/javascript')
        self.body = BODY(father = self.html)
        self.requires=[]

    def genHtmlTitle(self, title):
        self.title = TITLE(title, father=self.head)
    
    def controlrequires(self):
        d=dict()
        i = 0
        for e in self.requires:
            d[e] = f'p{i}'
            i += 1
        for e in ["ojs/ojbootstrap"]:
            if e not in d: raise Exception(f'"{e}" is a required library')
        return d

    
    def require(self, *elems):
        self.requires = list(elems)
        return self.controlrequires()
    
    def jupyter(self, width=800, height=450, name='jupyter.html'):
        from IPython.display import IFrame as ifr, display
        with open(f'./{name}', 'w') as f: f.write(self.render())
        display(ifr(f'./{name}', width=width, height=height))

    def render(self):
        
        CUSTOM = '''
                require({requires},
                function ({parameters})
                {{
                    {defclasses}
                    {boot}.whenDocumentReady().then(() => {{
                        {initcontainers}
                    }});
                }});
        '''
        dr = self.controlrequires()
        self.body.render()
        parameters = [f'p{i}' for i in range(len(self.requires))]
        dformat = dict(initcontainers='', requires=self.requires, defclasses='', boot=dr["ojs/ojbootstrap"] ,parameters=','.join(parameters))
        for c in self.body.containers:
            f = self.body.containers[c]
            dformat['initcontainers'] += f(c)
        for c in self.body.defclasses:
           dformat['defclasses'] += self.body.defclasses[c](c)
        self.script3 = SCRIPT(CUSTOM.format(**dformat), father=self.head, _type='text/javascript')
        return self.html.render()