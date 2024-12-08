from azure.functions import HttpRequest, HttpResponse
import numpy as np

def matmul(N):
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)

    C = np.matmul(A, B)

    return

def main(req: HttpRequest) -> HttpResponse:

    count = int(req.params.get('N'))
    matmul(count)

    return HttpResponse(
        status_code=200
    )
