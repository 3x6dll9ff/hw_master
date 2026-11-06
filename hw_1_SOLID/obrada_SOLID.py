import json
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Reservation:
    name: str
    nights: int
    price: float


class ReservationSource(Protocol):
    def load(self) -> list[Reservation]:
        ...


class ReportWriter(Protocol):
    def save(self, amounts: list[float]) -> None:
        ...


class Notifier(Protocol):
    def send(self, amounts: list[float]) -> None:
        ...


@dataclass
class CsvReservationSource:
    path: str

    def load(self) -> list[Reservation]:
        reservations = []

        with open(self.path) as file:
            for line in file:
                if not line.strip():
                    continue

                parts = line.strip().split(",")

                reservation = Reservation(
                    name=parts[0],
                    nights=int(parts[1]),
                    price=float(parts[2]),
                )
                reservations.append(reservation)

        return reservations


@dataclass
class JsonReservationSource:
    path: str

    def load(self) -> list[Reservation]:
        reservations = []

        with open(self.path) as file:
            data = json.load(file)

        for item in data:
            reservation = Reservation(
                name=item["name"],
                nights=item["nights"],
                price=item["price"],
            )
            reservations.append(reservation)

        return reservations


@dataclass
class TxtReportWriter:
    path: str

    def save(self, amounts: list[float]) -> None:
        with open(self.path, "w") as file:
            file.write(str(amounts))


class MailNotifier:
    def send(self, amounts: list[float]) -> None:
        print("Sent:", sum(amounts))


def calculate_amount(reservation: Reservation) -> float:
    return reservation.nights * reservation.price


class ReservationService:
    def __init__(
        self,
        source: ReservationSource,
        writer: ReportWriter,
        notifier: Notifier,
    ) -> None:
        self.source = source
        self.writer = writer
        self.notifier = notifier

    def process(self) -> list[float]:
        reservations = self.source.load()
        amounts = [calculate_amount(r) for r in reservations]
        self.writer.save(amounts)
        self.notifier.send(amounts)
        return amounts
