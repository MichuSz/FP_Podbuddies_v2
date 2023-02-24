from store.models import Device, Theme


def categories(request):
    devices = Device.objects.all().order_by('id')
    themes = Theme.objects.all().order_by('id')
    return  {'themes': themes, 'devices': devices}


