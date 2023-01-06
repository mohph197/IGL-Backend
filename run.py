from app import create_app,socketio
import os

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    socketio.run(app,host=os.environ['HOST_URL'])