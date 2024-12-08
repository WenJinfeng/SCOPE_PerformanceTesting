from azure.functions import HttpRequest, HttpResponse
import math


def float_operations(N):
    for i in range(0, N):
        sin_i = math.sin(i)
        cos_i = math.cos(i)
        sqrt_i = math.sqrt(i)
    return

def main(req: HttpRequest) -> HttpResponse:

    count = int(req.params.get('N'))
    float_operations(count)

    return HttpResponse(
        status_code=200
    )

