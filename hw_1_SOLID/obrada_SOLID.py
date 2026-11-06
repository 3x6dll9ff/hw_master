from typing import Protocol
from dataclasses import dataclass

@dataclass
class Reservation:
    name: str
    nights: int
    price: float

@dataclass
class CsvReservationSource:
    path: str

    def load(self) -> list[Reservation]:
        reservations = []

        with open(self.path) as file:
            for line in file:
                parts = line.strip().split(",")

                reservation = Reservation(
                    name = parts[0],
                    nights= int(parts[1]),
                    price= float(parts[2])
                )
                reservations.append(reservation)
        return reservations

@dataclass
class TxtReportWriter:
    path:str

    def save(self, amounts: list[float]) -> None:
        with open (self.path, "w") as file:
            file.write(str(amounts))


class MailNotifier:
    def send(self, amounts: list[float]) -> None:
        print("Sent:", sum(amounts))


class ReservationSource(Protocol):
    def load(self) -> list [Reservation]:
        ...

class ReportWriter(Protocol):
    def save(self, amounts: list[float]) -> None:
        ...


class Notifier(Protocol):
    def send(self, amounts: list[float]) -> None:
        ...



def calculate_amount(reservation: Reservation) -> float:
    return reservation.nights * reservation.price

