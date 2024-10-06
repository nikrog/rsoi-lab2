import datetime
import json
import uuid
from quart import Blueprint, Response, request
from reservation.models.models_class import ReservationModel

postreservationb = Blueprint('post_reservation', __name__, )


def validate_body(body):
    try:
        body = json.loads(body)
    except:
        return None, ['wrong']

    errors = []

    if (('hotelId' not in body or type(body['hotelId']) is not int) or (
            'startDate' not in body or type(body['startDate']) is not str) or (
            'endDate' not in body or type(body['endDate']) is not str) or (
            'paymentUid' not in body or type(body['paymentUid']) is not str)):
        return None, ['Bad structure body!']

    return body, errors


@postreservationb.route('/api/v1/reservations', methods=['POST'])
async def post_reservation() -> Response:
    if 'X-User-Name' not in request.headers.keys():
        return Response(status=400, content_type='application/json',
                        response=json.dumps({'errors': ['user not found']}))

    user = request.headers['X-User-Name']

    body, errors = validate_body(await request.body)
    if len(errors) > 0:
        return Response(status=400, content_type='application/json', response=json.dumps(errors))

    rental = ReservationModel.create(
        reservation_uid=uuid.uuid4(),
        username=user,
        payment_uid=uuid.UUID(body['paymentUid']),
        hotel_id=body['hotelId'],
        status='PAID',
        start_date=datetime.datetime.strptime(body['startDate'], "%Y-%m-%d").date(),
        end_date=datetime.datetime.strptime(body['endDate'], "%Y-%m-%d").date(),
    )

    return Response(status=200, content_type='application/json', response=json.dumps(rental.to_dict()))
