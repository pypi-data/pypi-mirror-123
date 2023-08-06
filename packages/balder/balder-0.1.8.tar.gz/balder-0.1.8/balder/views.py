from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.clickjacking import xframe_options_exempt

try:
    import channels_graphql_ws
    GraphQLView.graphiql_template = "balder/graphiql-ws.html"
except:
    GraphQLView.graphiql_template  = "balder/graphiql.html"
    pass


BalderView = xframe_options_exempt(csrf_exempt(GraphQLView.as_view(graphiql=True)))
BalderViewCsrfExempt = csrf_exempt(GraphQLView.as_view(graphiql=True))
BalderViewXFrameExempt = xframe_options_exempt(BalderViewCsrfExempt)