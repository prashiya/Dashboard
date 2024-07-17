from flask import Flask
from controllers import SalesController

app = Flask(__name__)

sales_controller = SalesController()


app.add_url_rule('/api/sales/total', 'total_sales', sales_controller.total_sales, methods=['GET'])
app.add_url_rule('/api/sales/by-category', 'sales_by_category', sales_controller.sales_by_category, methods=['GET'])
app.add_url_rule('/api/market-share/changes', 'market_share_changes', sales_controller.market_share_changes, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
