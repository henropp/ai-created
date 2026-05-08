from attendance_parser import apply_attendance_rules


def test_not_attended_is_skipped_status():
    data = {
        'training_date': '26/03/2026',
        'attendees': [
            {'name': 'Amie Jagne', 'signature_detected': True, 'notes': 'Not Attended'},
        ],
    }
    parsed = apply_attendance_rules(data)
    assert parsed['attendees'][0]['attendance_status'] == 'not_attended'
