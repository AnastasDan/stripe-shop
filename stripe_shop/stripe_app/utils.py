import stripe

from stripe_shop.settings import DOMAIN


def create_stripe_session(line_items, discounts=None):
    """Создает сеанс Stripe для оформления заказа."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=DOMAIN + "/success/",
            cancel_url=DOMAIN + "/cancel/",
            discounts=discounts,
        )

        return {"sessionId": session.id}

    except stripe.error.StripeError as e:
        return {"error": str(e)}
    except Exception:
        return {"error": "Internal Server Error"}, 500
