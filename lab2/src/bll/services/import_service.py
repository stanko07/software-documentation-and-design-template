"""Business-logic service that imports CSV data into the database."""

from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from src.bll.interfaces.i_import_service import IImportService
from src.dal.interfaces.i_city_repository import ICityRepository
from src.dal.interfaces.i_csv_reader import ICsvReader
from src.dal.interfaces.i_customer_repository import ICustomerRepository
from src.dal.interfaces.i_delivery_repository import IDeliveryRepository
from src.dal.interfaces.i_event_repository import IEventRepository
from src.dal.interfaces.i_order_repository import IOrderRepository
from src.dal.interfaces.i_payment_repository import IPaymentRepository
from src.dal.interfaces.i_ticket_type_repository import ITicketTypeRepository
from src.dal.interfaces.i_venue_repository import IVenueRepository
from src.models.orm_models import Delivery, Order, OrderItem, Payment


_DATE_FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]


def _parse_dt(value: str) -> datetime:
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: {value!r}")


def _parse_decimal(value: str) -> Decimal:
    try:
        return Decimal(value.strip())
    except InvalidOperation as exc:
        raise ValueError(f"Cannot parse decimal: {value!r}") from exc


class ImportService(IImportService):
    """
    Reads raw rows from the CSV via ICsvReader, constructs ORM models,
    and delegates persistence to the DAL repositories.

    All repository dependencies are injected via the constructor (IoC / DI).
    """

    def __init__(
        self,
        csv_reader: ICsvReader,
        city_repo: ICityRepository,
        venue_repo: IVenueRepository,
        event_repo: IEventRepository,
        ticket_type_repo: ITicketTypeRepository,
        customer_repo: ICustomerRepository,
        order_repo: IOrderRepository,
        payment_repo: IPaymentRepository,
        delivery_repo: IDeliveryRepository,
    ) -> None:
        self._csv_reader = csv_reader
        self._city_repo = city_repo
        self._venue_repo = venue_repo
        self._event_repo = event_repo
        self._ticket_type_repo = ticket_type_repo
        self._customer_repo = customer_repo
        self._order_repo = order_repo
        self._payment_repo = payment_repo
        self._delivery_repo = delivery_repo

    # ------------------------------------------------------------------
    # IImportService
    # ------------------------------------------------------------------

    def import_from_csv(self, file_path: str) -> int:
        imported = 0
        for row in self._csv_reader.read(file_path):
            try:
                self._import_row(row)
                imported += 1
            except Exception as exc:  # noqa: BLE001
                print(f"[WARN] Skipping row due to error: {exc} | row={row}")
        return imported

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _import_row(self, row: dict) -> None:
        # ── City ──────────────────────────────────────────────────────
        city = self._city_repo.get_or_create(row["city_name"])

        # ── Venue ─────────────────────────────────────────────────────
        venue = self._venue_repo.get_or_create(
            name=row["venue_name"],
            address=row["venue_address"],
            city_id=city.id,
        )

        # ── Event ─────────────────────────────────────────────────────
        event = self._event_repo.get_or_create(
            title=row["event_title"],
            date_time=_parse_dt(row["event_date_time"]),
            venue_id=venue.id,
        )

        # ── TicketType ────────────────────────────────────────────────
        ticket_type = self._ticket_type_repo.get_or_create(
            name=row["ticket_type_name"],
            price=_parse_decimal(row["ticket_price"]),
            available_count=int(row["ticket_available_count"]),
            event_id=event.id,
        )

        # ── Customer ──────────────────────────────────────────────────
        customer = self._customer_repo.get_or_create(
            full_name=row["customer_full_name"],
            email=row["customer_email"],
        )

        # ── Order ─────────────────────────────────────────────────────
        qty = int(row["order_item_qty"])
        unit_price = _parse_decimal(row["ticket_price"])
        total = unit_price * qty

        created_at = _parse_dt(row["order_created_at"])
        expires_at = created_at + timedelta(minutes=30)

        order = Order(
            status=row["order_status"],
            created_at=created_at,
            expires_at=expires_at,
            total=total,
            customer_id=customer.id,
        )
        order = self._order_repo.save(order)

        # ── OrderItem ─────────────────────────────────────────────────
        item = OrderItem(
            qty=qty,
            unit_price=unit_price,
            order_id=order.id,
            ticket_type_id=ticket_type.id,
        )
        self._order_repo.add_item(item)

        # ── Payment (optional) ────────────────────────────────────────
        if row.get("payment_provider"):
            paid_at_raw = row.get("payment_paid_at", "").strip()
            payment = Payment(
                status=row["payment_status"],
                provider=row["payment_provider"],
                paid_at=_parse_dt(paid_at_raw) if paid_at_raw else None,
                amount=total,
                order_id=order.id,
            )
            self._payment_repo.save(payment)

        # ── Delivery (optional) ───────────────────────────────────────
        if row.get("delivery_type"):
            sent_at_raw = row.get("delivery_sent_at", "").strip()
            delivery = Delivery(
                type=row["delivery_type"],
                status=row["delivery_status"],
                sent_at=_parse_dt(sent_at_raw) if sent_at_raw else None,
                order_id=order.id,
            )
            self._delivery_repo.save(delivery)
