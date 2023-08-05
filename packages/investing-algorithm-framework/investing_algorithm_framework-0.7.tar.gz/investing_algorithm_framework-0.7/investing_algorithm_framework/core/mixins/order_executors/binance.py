from investing_algorithm_framework.core.market_services import \
    BinanceMarketService
from investing_algorithm_framework.core.models import Order, OrderType, \
    OrderSide, db, OrderStatus
from investing_algorithm_framework.core.exceptions import OperationalException


class BinanceOrderExecutorMixin(BinanceMarketService):
    identifier = "BINANCE"

    def execute_limit_order(self, order: Order, algorithm_context, **kwargs):

        if not OrderType.LIMIT.equals(order.order_type):
            raise OperationalException(
                "Provided order is not a limit order type"
            )

        if OrderSide.BUY.equals(order.order_side):
            self.create_limit_buy_order(
                target_symbol=order.target_symbol,
                trading_symbol=order.trading_symbol,
                amount=order.amount,
                price=order.price
            )
        else:
            self.create_limit_sell_order(
                target_symbol=order.target_symbol,
                trading_symbol=order.trading_symbol,
                amount=order.amount,
                price=order.price
            )

    def execute_market_order(self, order: Order, algorithm_context, **kwargs):

        if not OrderType.MARKET.equals(order.order_type):
            raise OperationalException(
                "Provided order is not a market order type"
            )

        if OrderSide.BUY.equals(order.order_side):
            self.create_market_buy_order(
                target_symbol=order.target_symbol,
                trading_symbol=order.trading_symbol,
                amount=order.amount,
            )
        else:
            self.create_market_sell_order(
                target_symbol=order.target_symbol,
                trading_symbol=order.trading_symbol,
                amount=order.amount,
            )

    def get_order_status(self, order: Order, algorithm_context, **kwargs):
        order = self.get_order(
            order.exchange_id, order.target_symbol, order.trading_symbol
        )

        if order is not None:

            if order["info"]["status"] == "FILLED":
                return OrderStatus.SUCCESS.value

            if order["info"]["status"] == "REJECTED	":
                return OrderStatus.FAILED.value

            if order["info"]["status"] == "PENDING_CANCEL":
                return OrderStatus.FAILED.value

            if order["info"]["status"] == "EXPIRED":
                return OrderStatus.FAILED.value

            return OrderStatus.PENDING.value
