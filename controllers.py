from flask import request, jsonify
from datetime import datetime
import pandas as pd


class SalesController:
    def __init__(self):
       
        try:
            self.sales_data = pd.read_csv('sales_data.csv')
            self.category_share_data = pd.read_csv('category_share_data.csv')
            self.product_category_mapping = pd.read_csv('product_category_mapping.csv')
        except FileNotFoundError as e:
            
            raise Exception(f"Error loading data files: {str(e)}") from e
        except pd.errors.ParserError as e:
            
            raise Exception(f"Error parsing data files: {str(e)}") from e

    def total_sales(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Please provide both start_date and end_date"}), 400

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            
            self.sales_data['date'] = pd.to_datetime(self.sales_data['date'])

           
            filtered_data = self.sales_data[(self.sales_data['date'] >= start_date) & (self.sales_data['date'] <= end_date)]
            print(f"Number of entries in filtered data: {len(filtered_data)}")

            
            total_revenue = filtered_data['revenue'].sum().astype(float) * 2
            total_revenue = round(total_revenue, 2)  
            return jsonify({"total_revenue": total_revenue})
        except (ValueError, KeyError) as e:
            
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        except Exception as e:
            
            return jsonify({"error": "Internal server error"}), 500

    def sales_by_category(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Please provide both start_date and end_date"}), 400

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            
            self.sales_data['date'] = pd.to_datetime(self.sales_data['date'])

            
            filtered_data = self.sales_data[(self.sales_data['date'] >= start_date) & (self.sales_data['date'] <= end_date)]

            
            merged_data = filtered_data.merge(self.product_category_mapping, on='product_id')

            
            category_sales = merged_data.groupby('category_id').agg({'revenue': 'sum', 'quantity': 'sum'}).reset_index()
            return category_sales.to_json(orient='records')
        except (ValueError, KeyError) as e:
            
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        except Exception as e:
            
            return jsonify({"error": "Internal server error"}), 500

    def market_share_changes(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Please provide both start_date and end_date"}), 400

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

           
            self.category_share_data['date'] = pd.to_datetime(self.category_share_data['date'])

            
            filtered_data = self.category_share_data[(self.category_share_data['date'] >= start_date) & (self.category_share_data['date'] <= end_date)]

            
            market_share_changes = filtered_data.groupby('product_id').agg({'market_share': 'diff'}).astype(float).reset_index()

            
            market_share_changes.fillna(0, inplace=True)

            return market_share_changes.to_json(orient='records')
        except (ValueError, KeyError) as e:
           
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        except Exception as e:
            
            return jsonify({"error": "Internal server error"}), 500