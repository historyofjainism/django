from django import template
register = template.Library()

import content
import django.utils.html as html

@register.simple_tag
def link_li(article_name):
    title, subtitle, desc, img = content.get_summary( article_name )
    href = '/article/hi/' + article_name
    return html.format_html("""
        <a class='linkpreview' href='%(href)s'>
        <img style='float:left;width:100px;' src='%(img)s'/>
        <div>
            <div style="font-size:1em;">%(title)s</div>
            <div style="color: silver;font-size:0.75em;">%(subtitle)s</div>
        </div>
        </a>
    """ % locals())