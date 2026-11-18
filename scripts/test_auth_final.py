import os
import shutil
import sys
import tempfile

sys.path.insert(0, r"C:\Users\Admin\Desktop\NexusInsight")

data_dir = tempfile.mkdtemp(prefix="ni-auth-")
os.environ["DATA_DIR"] = data_dir
os.environ["APP_PASSWORD"] = "correct-horse-battery"
os.environ["APP_SECRET"] = "test-secret-material-that-is-stable"
os.environ["DEMO_MODE"] = "true"

try:
    from nexus_insight import create_app

    app = create_app()
    app.config.update(TESTING=True)

    with app.test_client() as client:
        r = client.get("/api/overview")
        print("unauth api:", r.status_code, r.headers.get("Location"))
        assert r.status_code in (302, 401)

        r = client.get("/")
        print("unauth page:", r.status_code, r.headers.get("Location"))
        assert r.status_code in (302, 401)

        r = client.get("/healthz")
        print("healthz:", r.status_code, r.get_json())
        assert r.status_code == 200

        r = client.get("/login")
        print("login page:", r.status_code, "Sign in" in r.get_data(as_text=True))
        assert r.status_code == 200

        r = client.post("/login", data={"password": "wrong"}, follow_redirects=False)
        print("bad login:", r.status_code)
        assert r.status_code == 200 and "Incorrect" in r.get_data(as_text=True)

        r = client.post("/login", data={"password": "correct-horse-battery"}, follow_redirects=False)
        print("good login:", r.status_code, r.headers.get("Location"))
        assert r.status_code == 302

        r = client.get("/api/overview")
        print("auth api:", r.status_code, r.headers.get("Content-Type"))
        assert r.status_code == 200

        settings = client.get("/api/settings").get_json()
        blob = str(settings).lower()
        for word in ("correct-horse-battery", "test-secret-material", "password"):
            if word in blob:
                print("!! secret leak marker:", word)
        print("settings keys:", sorted(settings)[:8])
        assert settings.get("app_auth_enabled") is True

        r = client.post("/logout", follow_redirects=False)
        print("logout:", r.status_code)
        r = client.get("/api/overview")
        print("post-logout api:", r.status_code)
        assert r.status_code in (302, 401)
    print("auth ok")
finally:
    shutil.rmtree(data_dir, ignore_errors=True)
