from backend.analyzer import analyze_lead

def test_healthcare_chatbot_inquiry():
    result = analyze_lead(
        "We need a healthcare chatbot for our website with multilingual support. "
        "Budget INR 200000 and launch in 2 months. It should integrate with our website."
    )
    assert result["industry"] == "Healthcare"
    assert result["budget"] is not None
    assert result["timeline"] is not None
    assert 0 <= result["lead_score"] <= 100
    assert result["priority"] in {"Low", "Medium", "High"}

def test_missing_information_is_reported():
    result = analyze_lead("We want a new website for our small company.")
    assert result["missing_information"]
    assert result["follow_up_questions"]

def test_rejects_short_input():
    try:
        analyze_lead("short")
    except ValueError:
        return
    assert False, "Expected ValueError"
