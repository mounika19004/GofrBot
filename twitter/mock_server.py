from flask import Flask, jsonify

app = Flask(__name__)

# Mock technology trends data
mock_tech_trends = [
    {
        "trends": [
            {
                "name": "#GoFr",
                "url": "http://twitter.com/search?q=%23GoFr",
                "promoted_content": None,
                "query": "%23AIForEveryone",
                "tweet_volume": 125678,
            },
            {
                "name": "#QuantumComputing",
                "url": "http://twitter.com/search?q=%23QuantumComputing",
                "promoted_content": None,
                "query": "%23QuantumComputing",
                "tweet_volume": 98654,
            },
            {
                "name": "ChatGPT-5",
                "url": "http://twitter.com/search?q=ChatGPT-5",
                "promoted_content": None,
                "query": "ChatGPT-5",
                "tweet_volume": 134780,
            },
            {
                "name": "#CyberSecurityAwareness",
                "url": "http://twitter.com/search?q=%23CyberSecurityAwareness",
                "promoted_content": None,
                "query": "%23CyberSecurityAwareness",
                "tweet_volume": 74562,
            },
            {
                "name": "#BlockchainRevolution",
                "url": "http://twitter.com/search?q=%23BlockchainRevolution",
                "promoted_content": None,
                "query": "%23BlockchainRevolution",
                "tweet_volume": 65892,
            },
        ]
    }
]

# Define a route for technology trends
@app.route("/1.1/trends/place.json", methods=['GET'])
def get_tech_trends():
    return jsonify(mock_tech_trends)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
