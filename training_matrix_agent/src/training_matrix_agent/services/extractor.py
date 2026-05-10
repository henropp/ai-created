
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import re
import base64
import io
import json

from training_matrix_agent.core.matching import normalize_name
from training_matrix_agent.models.schemas import AttendanceRecord, AttendanceStatus, ExtractionResult

from pdf2image import convert_from_path
from PIL import Image
from openai import OpenAI


class LLMPdfExtractor:
    """LLM-based extractor for scanned attendance forms."""

    def extract(self, pdf_path: Path) -> ExtractionResult:
        # Convert PDF to image
        images = convert_from_path(pdf_path)
        if not images:
            raise ValueError("Could not convert PDF to image.")
        
        # Assume the first page is the relevant one
        image = images[0]

        # Convert PIL Image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        client = OpenAI()

        response = client.chat.completions.create(
            model="gemini-2.5-flash", # Using gemini-2.5-flash as requested
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract the course name, training date, and a list of attendees with their attendance status (Attended or Not Attended) from this attendance form. For each attendee, provide their raw name and attendance status. If a signature is present, assume 'Attended'. If 'Not Attended' is explicitly written, use that. Otherwise, infer from context. Output in JSON format with keys: course_name (string), training_date (YYYY-MM-DD string), attendees (list of objects with raw_name (string) and status (string: 'Attended' or 'Not Attended'))."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_str}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )

        llm_output = response.choices[0].message.content
        
        # Attempt to parse the JSON output from the LLM
        try:
            extracted_data = json.loads(llm_output)
        except json.JSONDecodeError:
            # If LLM doesn't return perfect JSON, try to extract it using regex
            json_match = re.search(r"```json\n(.*?)```", llm_output, re.DOTALL)
            if json_match:
                try:
                    extracted_data = json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    raise ValueError(f"Could not parse JSON from LLM output: {llm_output}")
            else:
                raise ValueError(f"Could not find JSON in LLM output: {llm_output}")

        course_name = extracted_data.get("course_name", "Unknown Course")
        training_date_str = extracted_data.get("training_date")
        training_date = date.fromisoformat(training_date_str) if training_date_str else date.today()

        attendees: list[AttendanceRecord] = []
        for att_data in extracted_data.get("attendees", []):
            raw_name = att_data.get("raw_name", "")
            status_str = att_data.get("status", "Uncertain")
            
            status = AttendanceStatus.UNCERTAIN
            signature_present = False

            if status_str == "Attended":
                status = AttendanceStatus.ATTENDED
                signature_present = True
            elif status_str == "Not Attended":
                status = AttendanceStatus.NOT_ATTENDED
                signature_present = False
            
            if raw_name:
                attendees.append(
                    AttendanceRecord(
                        raw_name=raw_name,
                        normalized_name=normalize_name(raw_name),
                        status=status,
                        signature_present=signature_present,
                    )
                )

        return ExtractionResult(
            source_file=str(pdf_path),
            course_name=course_name,
            training_date=training_date,
            extracted_at=datetime.utcnow(),
            attendees=attendees,
        )
