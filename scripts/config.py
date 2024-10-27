# config.py

API_CONFIG = {
    "cellphoneS": {
        "url": "https://api.cellphones.com.vn/v2/graphql/query",
        "query": """
        query GetProductsByCateId {
            products(
                filter: {
                    static: {
                        categories: ["265"],
                        province_id: 30,
                        stock: {
                            from: 0
                        },
                        stock_available_id: [46, 56, 152, 4164],
                        filter_price: {
                            from: 0,
                            to: 13190000
                        }
                    },
                    dynamic: {}
                },
                size: 10000,
                sort: [{ view: desc }]
            ) {
                general {
                    product_id
                    name
                    attributes
                    sku
                    doc_quyen
                    manufacturer
                    url_key
                    url_path
                    categories {
                        categoryId
                    }
                    review {
                        total_count
                        average_rating
                    }
                },
                filterable {
                    is_installment
                    stock_available_id
                    company_stock_id
                    filter {
                        id
                        Label
                    }
                    is_parent
                    exclusive_prices
                    price
                    prices
                    special_price
                    promotion_information
                    thumbnail
                    promotion_pack
                    sticker
                    flash_sale_types
                }
            }
        }
        """
    }
}
