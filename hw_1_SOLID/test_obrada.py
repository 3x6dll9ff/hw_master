from pathlib import Path

import pytest

from obrada_SOLID import (
    CsvReservationSource,
    JsonReservationSource,
    MailNotifier,
    Reservation,
    ReservationService,
    TxtReportWriter,
    calculate_amount,
)


class FakeSource:
    def __init__(self, reservations: list[Reservation]) -> None:
        self.reservations = reservations

    def load(self) -> list[Reservation]:
        return self.reservations


class FakeWriter:
    def __init__(self) -> None:
        self.saved: list[float] = []

    def save(self, amounts: list[float]) -> None:
        self.saved = amounts


class FakeNotifier:
    def __init__(self) -> None:
        self.sent: list[float] = []

    def send(self, amounts: list[float]) -> None:
        self.sent = amounts


RESERVATIONS = [
    Reservation("Marko", 2, 50.0),
    Reservation("Ana", 3, 40.0),
]


def test_calculate_amount() -> None:
    reservation = Reservation("Marko", 2, 50.0)

    assert calculate_amount(reservation) == 100.0


def test_process_returns_amounts() -> None:
    service = ReservationService(
        FakeSource(RESERVATIONS), FakeWriter(), FakeNotifier()
    )

    assert service.process() == [100.0, 120.0]


def test_process_saves_and_notifies() -> None:
    writer = FakeWriter()
    notifier = FakeNotifier()
    service = ReservationService(FakeSource(RESERVATIONS), writer, notifier)

    service.process()

    assert writer.saved == [100.0, 120.0]
    assert notifier.sent == [100.0, 120.0]


def test_process_with_no_reservations() -> None:
    writer = FakeWriter()
    notifier = FakeNotifier()
    service = ReservationService(FakeSource([]), writer, notifier)

    assert service.process() == []
    assert writer.saved == []
    assert notifier.sent == []


def test_csv_source_loads_reservations(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text("Marko,2,50.0\nAna,3,40.0\n")

    assert CsvReservationSource(str(path)).load() == RESERVATIONS


def test_json_source_loads_reservations(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    path.write_text(
        '[{"name": "Marko", "nights": 2, "price": 50.0},'
        ' {"name": "Ana", "nights": 3, "price": 40.0}]'
    )

    assert JsonReservationSource(str(path)).load() == RESERVATIONS


def test_csv_source_skips_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text("Marko,2,50.0\n\nAna,3,40.0\n\n")

    assert CsvReservationSource(str(path)).load() == RESERVATIONS


def test_txt_report_writer_saves_amounts(tmp_path: Path) -> None:
    path = tmp_path / "report.txt"

    TxtReportWriter(str(path)).save([100.0, 120.0])

    assert path.read_text() == "[100.0, 120.0]"


def test_mail_notifier_prints_total(capsys: pytest.CaptureFixture[str]) -> None:
    MailNotifier().send([100.0, 120.0])

    assert capsys.readouterr().out == "Sent: 220.0\n"
