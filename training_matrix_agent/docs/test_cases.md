# Test Cases

1. **Happy path update**
   - Attendee attended, name matches, training date is newer/equal.
   - Expect proposed update and successful apply after approval.

2. **Not Attended is ignored**
   - Attendee marked `Not Attended`.
   - Expect skip; no Excel modification.

3. **Newer existing date protected**
   - Matrix has date later than attendance sheet date.
   - Expect skip in `skipped_newer_date`.

4. **Unknown staff not auto-created**
   - Name not found in matrix.
   - Expect unresolved name; route to `Needs Review`.

5. **Low-confidence fuzzy match flagged**
   - OCR typo gives weak match below threshold.
   - Expect unresolved name with confidence score.

6. **Approval denied**
   - Human rejects preview.
   - Expect no Excel update; move file to `Needs Review`.

7. **Audit trail completeness**
   - Confirm both `proposed_update` and terminal event are logged.
