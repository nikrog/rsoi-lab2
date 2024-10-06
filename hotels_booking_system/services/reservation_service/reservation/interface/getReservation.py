import json
from quart import Blueprint, Response, request
from reservation.models.models_class import ReservationModel

getreservationb = Blueprint('get_reservations', __name__,)


@getreservationb.route('/api/v1/reservations/<string:reservationUid>', methods=['GET'])
async def get_reservation(reservationUid: str) -> Response:
    if 'X-User-Name' not in request.headers.keys():
        return Response(status=400, content_type='application/json',
                        response=json.dumps({'errors': ['user not found']}))

    user = request.headers['X-User-Name']
    reservations = [reservation.to_dict() for reservation in ReservationModel.select().where((ReservationModel.username == user)
                                                                                             & (ReservationModel.uuid == reservationUid))]
    if not reservations:
        return Response(status=404, content_type='application/json',
                        response=json.dumps({'message': ['reservation not found']}))
    else:
        return Response(status=200, content_type='application/json', response=json.dumps(reservations))