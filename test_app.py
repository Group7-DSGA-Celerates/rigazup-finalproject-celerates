from streamlit.testing.v1 import AppTest
import time

def run_tests():
    print("Testing Cold Start...")
    at = AppTest.from_file("app.py")
    # Set secrets to mock Gemini API Key
    at.secrets["GEMINI_API_KEY"] = "mock_key"
    
    # Run the app
    at.run(timeout=30)
    if at.exception:
        print(f"Error on start: {at.exception[0]}")
        return
        
    print("Cold start OK. Pages available:")
    # Navigation is handled by AppTest if we just navigate or run.
    print(at.title)
    
    print("SUCCESS: No syntax/import errors on load.")

if __name__ == "__main__":
    run_tests()
