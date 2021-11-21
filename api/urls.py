from django.urls import path
from .views import (iotRelayRequestView,
                    iotRelayRequest2View,
                    iotRelayRequest3View,
                    iotRelayRequest4View,
                    iotRelayRequest5View,
                    iotRelayRequest6View,
                    iotRelayRequest7View,
                    iotRelayRequest8View,
                    iotRelayRequest9View,
                    iotRelayRequest10View)

urlpatterns = [
    path('kamar1/', iotRelayRequestView, name='kamar1'),
    path('kamar2/', iotRelayRequest2View, name='kamar2'),
    path('kamar3/', iotRelayRequest3View, name='kamar3'),
    path('kamar4/', iotRelayRequest4View, name='kamar4'),
    path('kamar5/', iotRelayRequest5View, name='kamar5'),
    path('kamar6/', iotRelayRequest6View, name='kamar6'),
    path('kamar7/', iotRelayRequest7View, name='kamar7'),
    path('kamar8/', iotRelayRequest8View, name='kamar8'),
    path('kamar9/', iotRelayRequest9View, name='kamar9'),
    path('kamar10/', iotRelayRequest10View, name='kamar10'),
]