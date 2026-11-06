# Mini project 1: Refactoring reservation processing

Refactoring of a monolithic reservation-processing class using the SOLID principles.

- `obrada_init.py`: the original script
- `obrada_SOLID.py`: the refactored version
- `test_obrada.py`: pytest tests

## Design

| Component | Responsibility |
|---|---|
| `Reservation` | Reservation data |
| `calculate_amount` | Amount calculation |
| `CsvReservationSource`, `JsonReservationSource` | Reading reservations from a file |
| `TxtReportWriter` | Saving the report to a text file |
| `MailNotifier` | Sending the total amount notification (currently simulated with `print`) |
| `ReservationService` | Coordinating the steps above |
| `ReservationSource`, `ReportWriter`, `Notifier` | Protocols that decouple the service from concrete implementations |

- **S:** each class or function has one reason to change.
- **D:** `ReservationService` depends only on Protocols, and its dependencies are passed in.
- **O:** `JsonReservationSource` was added without changing the service.

## Running the tests

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install pytest
.venv/bin/pytest hw_1_SOLID
```

## Work with AI

I used Claude Code as a tutor and assistant.

- **Application code:** I wrote it by hand, step by step. The assistant explained the concepts, suggested the code structure with examples, and reviewed each step. It also did the final formatting cleanup, moved the Protocols above the classes, and added skipping of blank lines in the CSV source.
- **Tests:** the assistant wrote them, including a test for blank CSV lines and tests for `TxtReportWriter` and `MailNotifier` added after a verification pass. I ran the first test, then asked it to finish the rest.
- **This README:** the assistant drafted it.

### Main prompts

The prompts below are paraphrased and translated from Russian.

- Explain the SOLID principles in programming.
- Guide me through this task step by step and explain the approach, so I can write the code myself.
- Translate the code and the task from Montenegrin to English.
- Why do we need a Protocol here?
- Check what we have done so far and tell me what comes next.
- Test everything first, then fix the gaps you found.

### Corrections made after review

- Renamed the `night` field to `nights`.
- Converted CSV values with `int()` and `float()`, because values read from a file are text.
- Built each `Reservation` from the parsed `parts` list instead of the object still being created.
- Renamed a Protocol from `MailNotifier` to `Notifier`, because the duplicate name replaced the real class.
- Corrected `MailNotifier.send` to print the total with `sum(amounts)` and removed an unnecessary `return`.
- Added the missing method calls and the `amounts` argument in `ReservationService.process`.
- Read JSON values from `item` by key instead of from `data` by index.

### My design decisions

- Used `@dataclass` for `CsvReservationSource` instead of the suggested handwritten `__init__`.
- Implemented the concrete classes first and extracted the Protocols from them afterwards, instead of starting with the Protocols as suggested.

### Comparison with the AI suggestion

The final design follows the structure the assistant suggested. The differences are the two decisions above. The corrections listed above were to my own code. The verification pass also found gaps in the assistant's work: blank CSV lines crashed the loader, and its tests did not cover `TxtReportWriter` or `MailNotifier`. Both were fixed.
