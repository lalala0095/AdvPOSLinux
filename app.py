import os
from app import create_app

# Create an instance of the app using the factory function
app = create_app()

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# # local testing
# if __name__ == "__main__":
#     app.run(debug=True)