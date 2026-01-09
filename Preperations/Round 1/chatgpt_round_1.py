from datamodel import OrderDepth, TradingState, Order
import json

class Trader:
    def run(self, state: TradingState):
        # Prepare a dictionary for our orders for each product
        result = {}

        # Retrieve current positions (default to 0 if not in state)
        current_positions = {}
        for product in state.order_depths.keys():
            current_positions[product] = state.position.get(product, 0)

        # Load persistent data (EMA and volatility estimates from previous tick)
        if state.traderData:
            # traderData is stored as a JSON string of our data dictionary
            data = json.loads(state.traderData)
        else:
            data = {}

        # Initialize data for any new product not seen before
        for product in state.order_depths.keys():
            if product not in data:
                # Use current mid-price as initial EMA and set initial vol to 0
                order_depth = state.order_depths[product]
                if order_depth.buy_orders and order_depth.sell_orders:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_ask = min(order_depth.sell_orders.keys())
                    initial_mid = (best_bid + best_ask) / 2.0
                elif order_depth.buy_orders:
                    initial_mid = max(order_depth.buy_orders.keys())
                elif order_depth.sell_orders:
                    initial_mid = min(order_depth.sell_orders.keys())
                else:
                    initial_mid = 0.0
                data[product] = {"ema": initial_mid, "vol": 0.0, "last_mid": initial_mid}

        # Iterate over each product's order book and decide orders
        for product, order_depth in state.order_depths.items():
            orders = []  # list to collect orders for this product

            # Skip if no orders on both sides (no market data)
            if not order_depth.buy_orders and not order_depth.sell_orders:
                result[product] = orders
                continue

            # Determine best bid and best ask with their volumes
            best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
            best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
            best_bid_vol = order_depth.buy_orders.get(best_bid, 0)
            best_ask_vol = order_depth.sell_orders.get(best_ask, 0)

            # Compute the microprice (volume-weighted mid-price) for current state
            if best_bid is not None and best_ask is not None and (best_bid_vol + best_ask_vol) > 0:
                microprice = (best_ask * best_bid_vol + best_bid * best_ask_vol) / (best_bid_vol + best_ask_vol)
            elif best_bid is not None and best_ask is not None:
                microprice = (best_bid + best_ask) / 2.0  # fallback to simple mid
            elif best_bid is not None:
                microprice = best_bid
            else:
                microprice = best_ask

            # Update moving average (EMA) and volatility estimate
            prev_ema = data[product]["ema"]
            prev_vol = data[product]["vol"]
            prev_mid = data[product]["last_mid"]
            # EMA with smoothing factor (alpha). A small alpha means a longer-term average.
            alpha = 0.1
            new_ema = prev_ema * (1 - alpha) + microprice * alpha
            # Volatility estimate: exponential moving average of absolute price changes
            beta = 0.1
            price_change = abs(microprice - prev_mid)
            new_vol = prev_vol * (1 - beta) + price_change * beta
            # Store updated values for next tick
            data[product]["ema"] = new_ema
            data[product]["vol"] = new_vol
            data[product]["last_mid"] = microprice

            # Calculate dynamic thresholds for trading triggers
            # Base threshold = max(spread, some multiple of volatility)
            spread = best_ask - best_bid if (best_ask is not None and best_bid is not None) else 0
            base_threshold = max(spread, 2 * new_vol)  # e.g. ~2*avg move
            # Adjust threshold based on trend (price vs EMA)
            # If price is above EMA (uptrend), use a tighter buy threshold and looser sell threshold.
            # If price is below EMA (downtrend), use tighter sell and looser buy threshold.
            if microprice > new_ema:
                # Uptrend: buy on smaller dips, sell only on larger spikes
                buy_threshold = 0.8 * base_threshold
                sell_threshold = 1.2 * base_threshold
            elif microprice < new_ema:
                # Downtrend: sell on smaller rises, buy on deeper dips
                buy_threshold = 1.2 * base_threshold
                sell_threshold = 0.8 * base_threshold
            else:
                # No strong trend
                buy_threshold = sell_threshold = base_threshold

            # Ensure a minimum threshold (avoid reacting to tiny moves)
            buy_threshold = max(buy_threshold, 1e-6)  # a tiny positive minimum
            sell_threshold = max(sell_threshold, 1e-6)

            # Decision: place buy order if best ask is sufficiently below fair price (EMA) 
            if best_ask is not None and best_ask < new_ema - buy_threshold:
                # Determine quantity to buy (all available at best ask, but respect position limit)
                buy_quantity = best_ask_vol
                # Cap the buy quantity to not exceed position limit
                max_buyable = 50 - current_positions.get(product, 0)  # position limit (e.g. 50)
                if buy_quantity > max_buyable:
                    buy_quantity = max_buyable
                if buy_quantity > 0:
                    orders.append(Order(product, best_ask, buy_quantity))
                    current_positions[product] += buy_quantity  # update current position

            # Decision: place sell order if best bid is sufficiently above fair price
            if best_bid is not None and best_bid > new_ema + sell_threshold:
                sell_quantity = best_bid_vol
                # Cap the sell quantity to not exceed short position limit
                max_sellable = current_positions.get(product, 0) + 50  # how much we can sell without going below -50
                if sell_quantity > max_sellable:
                    sell_quantity = max_sellable
                if sell_quantity > 0:
                    orders.append(Order(product, best_bid, -sell_quantity))
                    current_positions[product] -= sell_quantity

            # Add this product's orders to result
            result[product] = orders

        # Save our updated indicators back into traderData (as JSON string) for next tick
        return result, 0, json.dumps(data)
