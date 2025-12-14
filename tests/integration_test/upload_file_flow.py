def test_integration_upload_flow(client):
    login_payload = {"username": "admin", "password": "admin"}
    response = client.post("/auth/token", json=login_payload)
    assert response.status_code == 200
    token = response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    csv_content = b"""transaction_id,date,category,amount,currency
TXN1,2025-01-01,Food,100.5,USD
TXN2,2025-01-02,Transport,20.0,USD"""

    files = {
        'file': ('test_data.csv', csv_content, 'text/csv')
    }

    response = client.post("/v1/files/upload", files=files, headers=headers)

    assert response.status_code == 200
    data = response.json()["data"]

    assert data["filename"] == "test_data.csv"
    assert "file_id" in data
    assert "upload_time" in data

    file_id = data["file_id"]
    summary_res = client.get(f"/v1/files/{file_id}/summary", headers=headers)
    assert summary_res.status_code == 200
    summary_data = summary_res.json()["data"]
    assert summary_data["total_transactions"] == 2
    assert summary_data["total_amount"] == 120.5