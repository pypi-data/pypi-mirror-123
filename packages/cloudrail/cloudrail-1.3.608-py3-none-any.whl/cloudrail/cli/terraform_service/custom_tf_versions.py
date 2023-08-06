def get_custom_tf_versions():
    return {"versions":
                {"0.12": "51",
                 "0.13": "44",
                 "0.14": "48",
                 "0.15": "28",
                 "1.0": "22"},
            "architectures": {
                "0.12": ["linux-amd64", "darwin-amd64", "windows-amd64"],
                "0.13": ["linux-amd64", "darwin-amd64", "windows-amd64"],
                "0.14": ["linux-amd64", "darwin-amd64", "windows-amd64"],
                "0.15": ["linux-amd64", "linux-arm64", "darwin-amd64", "darwin-arm64", "windows-amd64"],
                "1.0": ["linux-amd64", "linux-arm64", "darwin-amd64", "darwin-arm64", "windows-amd64"]}}
