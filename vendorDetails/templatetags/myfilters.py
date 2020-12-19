from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    st=value.label_tag()+''
    placehollderstr= st[st.index(">")+1: st.index("</")]
    return value.as_widget(attrs={'class': arg, 'placeholder': placehollderstr})
@register.filter(name='addplaceholder')
def addplaceholder(value, arg):
    return value.as_widget(attrs={'placeholder': str(arg.data)})