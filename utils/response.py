from rest_framework.response import Response


class SuccessResponse:
    @staticmethod
    def create(data=None, message="Success", status_code=200):
        return Response(
            {
                "status": "success",
                "message": message,
                "data": data,
            },
            status=status_code,
        )