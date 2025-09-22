import argparse
import json
from src.services import product_service, customer_service, order_service, reporting_service
from src.dao import product_dao, customer_dao

class CLIApp:
    """Retail CLI Application"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="retail-cli")
        self.subparsers = self.parser.add_subparsers(dest="cmd")
        self.prod_service = product_service.ProductService()
        self.cust_service = customer_service.CustomerService()
        self.report_service = reporting_service.ReportingService()
        self._build_commands()

    # ------------------------
    # Product Handlers
    # ------------------------
    def product_add(self, args):
        try:
            p = self.prod_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
            print("Created product:")
            print(json.dumps(p, indent=2))
        except product_service.ProductError as e:
            print("Error:", e)

    def product_list(self, args):
        ps = self.prod_service.list_all_products()
        print(json.dumps(ps, indent=2))

    # ------------------------
    # Customer Handlers
    # ------------------------
    def customer_add(self, args):
        try:
            c = self.cust_service.add_customer(args.name, args.email, args.phone, args.city)
            print("Created customer:")
            print(json.dumps(c, indent=2))
        except customer_service.CustomerError as e:
            print("Error:", e)

    def customer_list(self, args):
        cs = self.cust_service.list_customers()
        print(json.dumps(cs, indent=2))

    # ------------------------
    # Reporting Handlers
    # ------------------------
    def report_top_products(self, args):
        data = self.report_service.top_selling_products()
        print("Top Selling Products:")
        print(json.dumps(data, indent=2))

    def report_total_revenue(self, args):
        revenue = self.report_service.total_revenue_last_month()
        print(f"Total Revenue Last Month: {revenue}")

    def report_orders_per_customer(self, args):
        data = self.report_service.orders_per_customer()
        print("Orders per Customer:")
        print(json.dumps(data, indent=2))

    def report_frequent_customers(self, args):
        data = self.report_service.frequent_customers()
        print("Frequent Customers:")
        print(json.dumps(data, indent=2))

    # ------------------------
    # CLI Parser Setup
    # ------------------------
    def _build_commands(self):
        # Product
        p_prod = self.subparsers.add_parser("product", help="product commands")
        pprod_sub = p_prod.add_subparsers(dest="action")

        addp = pprod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category")
        addp.set_defaults(func=self.product_add)

        listp = pprod_sub.add_parser("list")
        listp.set_defaults(func=self.product_list)

        # Customer
        pcust = self.subparsers.add_parser("customer", help="customer commands")
        pcust_sub = pcust.add_subparsers(dest="action")

        addc = pcust_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city")
        addc.set_defaults(func=self.customer_add)

        listc = pcust_sub.add_parser("list")
        listc.set_defaults(func=self.customer_list)

        # Reporting
        prep = self.subparsers.add_parser("report", help="report commands")
        rsub = prep.add_subparsers(dest="action")

        rtop = rsub.add_parser("top-products")
        rtop.set_defaults(func=self.report_top_products)

        rrev = rsub.add_parser("revenue")
        rrev.set_defaults(func=self.report_total_revenue)

        rorders = rsub.add_parser("orders-per-customer")
        rorders.set_defaults(func=self.report_orders_per_customer)

        rfreq = rsub.add_parser("frequent-customers")
        rfreq.set_defaults(func=self.report_frequent_customers)

    # ------------------------
    # Run
    # ------------------------
    def run(self):
        args = self.parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            self.parser.print_help()

if __name__ == "__main__":
    CLIApp().run()
